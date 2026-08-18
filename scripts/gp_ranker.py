from functools import total_ordering
USAGE = f"""
#############################################################################################################################
# This script scrapes the GP rankings of Indian puzzlers from the World Puzzle Federation website.                          #
# It fetches the rankings from the preliminary results page for each round of the GP and prints them in a formatted manner. #
# Note: send the num_rounds as a command-line argument and work for only the first num_rounds                               #
#############################################################################################################################
"""

###########
# Imports #
###########
import requests
import json
from bs4 import BeautifulSoup
from argparse import ArgumentParser as ArgParser
#############
# Constants #
#############
BASE_URL = "https://gp.worldpuzzle.org/content/preliminary-results-wpf-gp-puzzle-"           
BASE_URL_v2 = "https://gp.worldpuzzle.org/WPF_scripts/RL_GP_v00.php?game_type=WPF_GP26_P_t" #followed by round number e.g. 1,2,3,4,5...
parser = ArgParser(description=USAGE)
parser.add_argument('--num_rounds', type=int, default=5, help='Number of rounds to fetch rankings for (default: 5)')

####################
#     Classes      #
####################


class Puzzler():
    def __init__(self, name: str, country: str, points: list = None ):
        self.name    = name
        self.country = country
        self.points  = points

    def __repr__(self):
        pts = f' {", ".join(map(str, self.points))}'
        return f"Puzzler(name={self.name}, points={pts})\n"

####################
# Helper Functions #
####################
def get_gp_rankings_of_India(url: str) -> list:
    """
    Get the GP rankings of India from the given URL.

    Args:
        url (str): The URL to fetch the GP rankings from.

    Returns:
        list: A list of dictionaries containing the GP rankings.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # the GP rankings are in a table with a specific class
    table = soup.find('table', {'class': 'playerstab'})
    rows = table.find_all('tr')[1:]  # Skip the header row

    rankings = []
    for row in rows:
        cols = row.find_all('td')
        try:
            ranking = {  
                    'country': cols[2].text.strip(), #country name 
            }
            if ranking['country'] in ('India', 'in'):
                ranking['name'] = cols[1].text.strip() # puzzler name
                ranking['points'] = int(cols[4].text.strip()) #points scored
                rankings.append(ranking)
        except IndexError:
            continue

    return rankings


def get_gp_rankings_of_India_v2(url: str) -> list:
    """
    Get the GP rankings of India from the given URL.

    Args:
        url (str): The URL to fetch the GP rankings from.

    Returns:
        list: A list of dictionaries containing the GP rankings.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # the GP rankings are in a table with a specific class
    table = soup.find('table', {'class': 'playerstab'})
    rows = table.find_all('tr')[1:]  # Skip the header row

    rankings = []
    for row in rows:
        cols = row.find_all('td') 
        try:
            ranking = {  
                    'country': cols[2].text.strip(), #country name 
            }
            if ranking['country'] in ('India', 'in'):
                ranking['name'] = cols[1].text.strip() # puzzler name
                
                score = cols[-4].text.strip() #points scored
                #if points scored is empty, set it to 0
                if score in ('', '-'): 
                    ranking['points'] = 0
                else:   
                    ranking['points'] = score
                rankings.append(ranking)
        except IndexError:
            continue

    return rankings

#################
# main function #
#################
def main():
    dict_Indian_puzzlers = dict() # dictionary to store the unique puzzlers across rounds

    def print_rankings(rankings: list):
        '''
        Print the GP rankings in a formatted manner.
        '''

        for rank, ranking in enumerate(rankings, start=1):
            # pretty print the rankings of Indian puzzlers, with evenly spaced columns
            print(f"{rank}. {ranking['name']:<20} {ranking['country']:<10} {ranking['points']:<10}")


    def iterate_over_rankings(num: int=5 ):
        '''
        Iterate over the GP rankings for the given number of rounds and print them.
        '''
        for round in range(1, num + 1): 
            print(f"GP Rankings of India for Round {round}:\n")
            rankings = get_gp_rankings_of_India_v2(BASE_URL_v2 + f"{round}")
            #print_rankings(rankings)
            list_of_Puzzlers = save_rankings(rankings, round)
            print(f"\nList of Puzzlers for Round {round}:")
            for puzzler in list_of_Puzzlers:
                #print(f"  {puzzler.name} ({puzzler.country}): {puzzler.points}")
                if puzzler.name not in dict_Indian_puzzlers:
                    dict_Indian_puzzlers[puzzler.name] = (puzzler.name, puzzler.country, [puzzler.points]) # store the points in a list
                else:
                    # if the puzzler is already in the dictionary, add the points in the list of points to the existing points in the dictionary
                    dict_Indian_puzzlers[puzzler.name][2].append(puzzler.points)
                    print(f"Updated points for {puzzler.name}: {dict_Indian_puzzlers[puzzler.name][2]}")
            print("\n" + "="*50 + "\n") # separator between rounds
        

    def save_rankings(rankings: list, round: int):
        ''' 
        Save the GP rankings of India into a list of Puzzler objects for the given round.
        '''
        list_of_Puzzlers = []
        for ranking in rankings:
            puzzler = Puzzler(
                name=ranking['name'],
                country=ranking['country'],
                points=ranking['points']
            )
            list_of_Puzzlers.append(puzzler)
        return list_of_Puzzlers

    def print_puzzlers():
        '''
        Print the unique puzzlers across all rounds.
        '''
        print(f"\nUnique Puzzlers across all rounds:\n")
        for name, (name, country, points) in dict_Indian_puzzlers.items():
            print(f"{name:<20} {country:<10} {points}")

    # Steps 
    iterate_over_rankings() # only first 5 rounds
    print_puzzlers()        # print the unique puzzlers across all rounds
    

if __name__ == "__main__":
    try:
        print(f"{USAGE}")
        args = parser.parse_args()
        num_rounds = args.num_rounds
        main(num_rounds)
    except TypeError:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")