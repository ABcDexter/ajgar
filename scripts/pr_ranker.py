#############################################################################################################################
# This script scrapes the Puzzle Ramayan (PR) rankings from the Logic Masters India page and
# prints a concise summary (including ranks and marks). It also writes a JSON output for further use.
#############################################################################################################################

###########
# Imports #
###########
import requests
import json
import argparse
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional

#############
# Constants #
#############
PR_URL = "https://logicmastersindia.com/PR/2026-ranks.asp"
OUTPUT_FILE = "pr_ranker_output.json"
DEFAULT_TOP_N = 20

####################
# Helper Functions #
####################
def _text_or_empty(el) -> str:
    return el.text.strip() if el else ""


def fetch_page(url: str) -> str:
    """
    Fetch the HTML content at `url` and return the text.
    """
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text


def parse_result_tables(html: str) -> List[Dict[str, Any]]:
    """
    Parse all HTML tables on the page and return a list of table-data dictionaries.

    Each table dict contains:
      - title: optional title (from nearest heading)
      - headers: list of header names
      - rows: list of dicts mapping header->cell text
    """
    soup = BeautifulSoup(html, "html.parser")

    tables = soup.find_all("table")
    parsed = []

    for idx, table in enumerate(tables, start=1):
        # attempt to find a nearby heading as title
        title = None
        for heading_tag in ("h1", "h2", "h3", "h4", "h5", "caption"):
            heading = table.find_previous(heading_tag)
            if heading:
                title = _text_or_empty(heading)
                break

        # extract headers
        headers = []
        header_row = table.find("tr")
        if header_row:
            ths = header_row.find_all("th")
            if ths:
                headers = [h.text.strip() for h in ths]

        # if no <th>, try to deduce headers from first row's cells (fallback)
        rows = []
        trs = table.find_all("tr")
        start_i = 0
        if headers:
            start_i = 1
        elif trs:
            # use first row as headers if it looks like header names (non-numeric)
            first_cols = trs[0].find_all(["td", "th"]) or []
            guess_headers = [c.text.strip() for c in first_cols]
            if any(guess_headers):
                # adopt guessed headers and skip first row
                headers = guess_headers
                start_i = 1

        for tr in trs[start_i:]:
            cols = tr.find_all(["td", "th"])
            if not cols:
                continue
            # map cell text to header if available, otherwise use index-based keys
            row = {}
            for i, cell in enumerate(cols):
                key = headers[i] if i < len(headers) else f"col_{i}"
                row[key] = cell.text.strip()
            rows.append(row)

        parsed.append({
            "title": title or f"Table {idx}",
            "headers": headers,
            "rows": rows,
        })

    return parsed


def find_country_column(headers: List[str]) -> Optional[str]:
    """
    Heuristically find the header name that corresponds to the country column.
    Returns the header string or None.
    """
    if not headers:
        return None

    low = [h.lower() for h in headers]
    for kw in ("country", "nat", "nation", "team", "cntry"):
        for h in headers:
            if kw in h.lower():
                return h
    return None


def find_name_column(headers: List[str]) -> Optional[str]:
    if not headers:
        return None
    for h in headers:
        if any(k in h.lower() for k in ("name", "participant", "player")):
            return h
    return None


def find_score_column(headers: List[str]) -> Optional[str]:
    if not headers:
        return None
    for h in headers:
        if any(k in h.lower() for k in ("score", "marks", "points", "total")):
            return h
    return None


def filter_india_rows(rows: List[Dict[str, str]], country_col: Optional[str]) -> List[Dict[str, str]]:
    """
    Return rows where the country column indicates India. If no country_col is found,
    return an empty list (no filtering possible).
    """
    if not country_col:
        return []
    indian = []
    for r in rows:
        val = r.get(country_col, "").strip().lower()
        if val in ("india", "in"):
            indian.append(r)
    return indian


#################
# main function #
#################
def main():
    # parse command line args
    parser = argparse.ArgumentParser(description="Scrape Puzzle Ramayan ranks and print summaries.")
    parser.add_argument('--TOP_N', type=int, default=DEFAULT_TOP_N,
                        help='Number of top rows to print when no Indian participants are present (<=0 to print all).')
    args = parser.parse_args()
    TOP_N = args.TOP_N

    def print_rankings_table(table: Dict[str, Any]):
        """
        Nicely print the rows from a parsed table, highlighting Indian participants.
        """
        title = table.get("title")
        headers = table.get("headers", [])
        rows = table.get("rows", [])

        print(f"{title}\n")

        country_col = find_country_column(headers)
        name_col = find_name_column(headers) or (headers[0] if headers else "name")
        score_col = find_score_column(headers)

        # If we can find Indian participants, print only them; otherwise print top rows
        india_rows = filter_india_rows(rows, country_col)

        if india_rows:
            to_print = india_rows
        else:
            # TOP_N <= 0 means print all rows
            to_print = rows if TOP_N <= 0 else rows[:TOP_N]

        # print header for convenience
        hdr_name = name_col or "Name"
        hdr_country = country_col or "Country"
        hdr_score = score_col or "Score"
        print(f"{'#':<4} {hdr_name:<30} {hdr_country:<10} {hdr_score:<8}")
        print("-" * 60)

        for i, r in enumerate(to_print, start=1):
            name = r.get(hdr_name, r.get(list(r.keys())[0], "")).strip()
            country = r.get(hdr_country, "").strip()
            score = r.get(hdr_score, "").strip() if hdr_score in r else ""
            print(f"{i-1:<4} {name:<30} {country:<10} {score:<8}")

        print("\n")

    html = fetch_page(PR_URL)
    tables = parse_result_tables(html)

    # print each parsed table
    for table in tables:
        print_rankings_table(table)

    # write output json for later consumption
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
            json.dump(tables, fh, ensure_ascii=False, indent=2)
        print(f"Wrote parsed results to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Failed to write output file: {e}")


if __name__ == "__main__":
    main()
