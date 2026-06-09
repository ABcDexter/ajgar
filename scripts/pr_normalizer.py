#############################################################################################################################
# This script fetches Round 5 live scores for Puzzle Ramayan, normalizes Indian participants
# so that the 4th-highest Indian score maps to 100, and writes a combined JSON file
# `pr_ranker_final.json` containing the first 4 rounds (read from `pr_ranker_output.json`)
# plus the normalized Round 5 data.
#############################################################################################################################

###########
# Imports #
###########
import requests
import json
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
import math

#############
# Constants #
#############
ROUND5_URL = "https://logicmastersindia.com/live/score?contest=PR202605"
INPUT_FILE = "pr_ranker_output.json"
OUTPUT_FILE = "pr_ranker_final.json"


####################
# Helper Functions #
####################
def fetch_url(url: str) -> requests.Response:
    r = requests.get(url)
    r.raise_for_status()
    return r


def _is_participant_list(obj: Any) -> bool:
    """
    Heuristic: obj is a list of dicts with name and score/total keys.
    """
    if not isinstance(obj, list) or not obj:
        return False

    # find at least one dict element with name-like and score-like key
    for el in obj:
        if not isinstance(el, dict):
            continue
        keys = [k.lower() for k in el.keys()]
        if any(k in keys for k in ("name", "player", "participant")) and any(k in keys for k in ("score", "total", "marks", "points")):
            return True
    return False


def _find_candidate_list(obj: Any):
    """
    Recursively search JSON-like structure for a candidate participant list.
    """
    if _is_participant_list(obj):
        return obj
    if isinstance(obj, dict):
        for v in obj.values():
            res = _find_candidate_list(v)
            if res is not None:
                return res
    elif isinstance(obj, list):
        for v in obj:
            res = _find_candidate_list(v)
            if res is not None:
                return res
    return None


def extract_participants_from_json(data: Any) -> List[Dict[str, Any]]:
    lst = _find_candidate_list(data)
    if not lst:
        return []

    out = []
    for el in lst:
        if not isinstance(el, dict):
            continue
        
        # gather name
        name = el.get("name") or el.get("player") or el.get("participant") or el.get("displayName") or el.get("username")
        
        # gather country
        country = el.get("country") or el.get("nation") or el.get("nat") or el.get("team")
        
        # gather score
        score = el.get("score") or el.get("total") or el.get("marks") or el.get("points")
        
        # normalize types
        try:
            score_f = float(score) if score not in (None, "") else 0.0
        except Exception:
            # sometimes score is a string with non-numeric chars
            try:
                score_f = float(str(score).strip())
            except Exception:
                score_f = 0.0

        out.append({
            "name": str(name).strip() if name is not None else "",
            "country": str(country).strip() if country is not None else "",
            "score": score_f,
            "raw": el,
        })

    return out


def extract_participants_from_html(html: str) -> List[Dict[str, Any]]:
    '''
    Heuristic HTML parsing: look for tables, try to deduce headers, and extract rows.
    Let's look for columns that resemble name, country, and score based on header keywords.
    This is a best-effort approach and may not be perfect.
    '''
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")
    for table in tables:
        # try to deduce headers
        headers = [th.text.strip() for th in table.find_all("th")]
        trs = table.find_all("tr")
        rows = []
        for tr in trs:
            cols = tr.find_all(["td", "th"])
            if not cols:
                continue
            texts = [c.text.strip() for c in cols]
            rows.append(texts)
        # if we have headers and rows, attempt mapping
        if headers and rows:
            key_idx = {h.lower(): i for i, h in enumerate(headers)}
            name_idx = None
            score_idx = None
            country_idx = None
            for h, i in key_idx.items():
                if any(k in h for k in ("name", "player", "participant")):
                    name_idx = i
                if any(k in h for k in ("score", "marks", "total", "points")):
                    score_idx = i
                if any(k in h for k in ("country", "nat", "nation", "team")):
                    country_idx = i

            out = []
            for r in rows:
                name = r[name_idx] if name_idx is not None and name_idx < len(r) else ""
                country = r[country_idx] if country_idx is not None and country_idx < len(r) else ""
                score_s = r[score_idx] if score_idx is not None and score_idx < len(r) else "0"
                try:
                    score_f = float(score_s) if score_s not in ("", "-") else 0.0
                except Exception:
                    score_f = 0.0
                out.append({"name": name, "country": country, "score": score_f, "raw": r})
            if out:
                return out

    # fallback: no table found
    return []


def fetch_round5_indian_scores(url: str) -> List[Dict[str, Any]]:
    '''
    Fetch live scores from the given URL, extract participant data, and filter for Indian participants.
    '''
    r = fetch_url(url)
    # try JSON
    try:
        data = r.json()
        participants = extract_participants_from_json(data)
        if participants:
            # filter India
            print(f"Found {len(participants)} participants in JSON data, filtering for India...")
            india = [p for p in participants if str(p.get("country", "")).strip().lower() in ("india", "in")]
            return india
    except ValueError:
        participants = []

    # try HTML fallback
    participants = extract_participants_from_html(r.text)
    print(f"Found {len(participants)} participants in HTML data, filtering for India...")
    india = [p for p in participants if str(p.get("country", "")).strip().lower() in ("india", "in")]
    return india


def normalize_scores(participants: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    '''
    Normalize scores so that the 4th-highest Indian score maps to 100. 
    If fewer than 4 participants, use the last available.
    '''
    # sort descending by score
    sorted_p = sorted(participants, key=lambda x: x.get("score", 0.0), reverse=True)
    scores = [p.get("score", 0.0) for p in sorted_p]
    if not scores:
        return []

    # choose 4th highest or last available if fewer than 4
    if len(scores) >= 4:
        s4 = scores[3]
    else:
        s4 = scores[-1]

    factor = 0.0
    if s4 and not math.isclose(s4, 0.0):
        factor = 100.0 / s4

    out = []
    for rank, p in enumerate(sorted_p, start=1):
        score = p.get("score", 0.0)
        norm = score * factor if factor else 0.0
        out.append({
            "rank": rank,
            "name": p.get("name", ""),
            "country": p.get("country", ""),
            "score": score,
            "normalized": round(norm, 3),
        })
    return out


#################
# main function #
#################
def main():
    # load existing pr_ranker_output.json
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception as e:
        print(f"Failed to read {INPUT_FILE}: {e}")
        return

    # keep first 4 tables (or all available up to 4)
    first_four = data[:4]

    # fetch round5 Indian scores
    print("Fetching Round 5 live scores...")
    india_scores = fetch_round5_indian_scores(ROUND5_URL)
    if not india_scores:
        print("No Indian participants found in Round 5 (or failed to parse live data).")

    normalized = normalize_scores(india_scores)

    # build round5 table
    round5_table = {
        "title": "Round 5 (Normalized)",
        "headers": ["Rank", "Name", "Country", "Score", "Normalized"],
        "rows": []
    }
    for r in normalized:
        round5_table["rows"].append({
            "Rank": str(r["rank"]),
            "Name": r["name"],
            "Country": r["country"],
            "Score": str(r["score"]),
            "Normalized": str(r["normalized"]),
        })

    final = list(first_four)
    final.append(round5_table)

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
            json.dump(final, fh, ensure_ascii=False, indent=2)
        print(f"Wrote combined results to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Failed to write {OUTPUT_FILE}: {e}")


if __name__ == "__main__":
    main()
