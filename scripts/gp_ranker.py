#############################################################################################################################
# This script scrapes the GP rankings of Indian puzzlers from the World Puzzle Federation website.                          #
# It fetches the rankings from the preliminary results page for each round of the GP and prints them in a formatted manner. #
# Note: The script currently only works for round 5 due to login requirements for earlier rounds.                           #
#############################################################################################################################

###########
# Imports #
###########
import requests
import json
from bs4 import BeautifulSoup

#############
# Constants #
#############
BASE_URL = "https://gp.worldpuzzle.org/content/preliminary-results-wpf-gp-puzzle" 

####################
# Helper Functions #
####################
def get_gp_rankings_of_india(url: str) -> list:
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

#################
# main function #
#################
def main():
    
    def print_rankings(rankings: list):
        '''
        Print the GP rankings in a formatted manner.
        '''
        
        for rank, ranking in enumerate(rankings, start=1):
            # pretty print the rankings of Indian puzzlers, with evenly spaced columns
            print(f"{rank}. {ranking['name']:<20} {ranking['country']:<10} {ranking['points']:<10}")


    def iterate_over_rankings(num: int):
        '''
        Iterate over the GP rankings for the given number of rounds and print them.
        '''
        for round in [5]: #range(1, num + 1): #doesn't work for rounds 1-4, login creds??
            rankings = get_gp_rankings_of_india(BASE_URL + f"-{round}")
            print_rankings(rankings)
        
    iterate_over_rankings(5) #onyl first 5 rounds


if __name__ == "__main__":
    main()