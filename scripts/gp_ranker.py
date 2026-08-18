
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
        self.best_three = None

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
            #print(f"GP Rankings of India for Round {round}:\n")
            rankings = get_gp_rankings_of_India_v2(BASE_URL_v2 + f"{round}")
            #print_rankings(rankings)
            list_of_Puzzlers = save_rankings(rankings, round)
            #print(f"\nList of Puzzlers for Round {round}:")
            for puzzler in list_of_Puzzlers:
                #print(f"  {puzzler.name} ({puzzler.country}): {puzzler.points}")
                if puzzler.name not in dict_Indian_puzzlers:
                    dict_Indian_puzzlers[puzzler.name] = (puzzler.name, puzzler.country, [puzzler.points]) # store the points in a list
                else:
                    # if the puzzler is already in the dictionary, add the points in the list of points to the existing points in the dictionary
                    dict_Indian_puzzlers[puzzler.name][2].append(puzzler.points)
                    #print(f"Updated points for {puzzler.name}: {dict_Indian_puzzlers[puzzler.name][2]}")
            #print("\n" + "="*50 + "\n") # separator between rounds
        

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

    def sort_points():
        '''
        Sort the points of each puzzler across rounds.
        '''
        for name, (name, country, points) in dict_Indian_puzzlers.items():
            points.sort(reverse=True) # sort the points in descending order
            #print(f"Sorted points for {name}: {points}")

    def normalize_scores():
        '''
        Take the best 3 scores of each puzzler, sum them up to make a best_three, and normalize the scores by giving the 4th highest best_three score a value of 100, and the rest of the scores are scaled accordingly. The normalized scores are stored in a new attribute of the Puzzler class called best_three.
        '''
        list_of_puzzlers = []
        for name, (name, country, points) in dict_Indian_puzzlers.items():
            best_three = sum(int(point) for point in points[:3]) # take the best 3 scores
            list_of_puzzlers.append([name,best_three])

        # sort the list of puzzlers by best_three in descending order
        list_of_puzzlers.sort(key=lambda x: x[1], reverse=True)

        print(f" List of Puzzlers sorted by best_three:\n {list_of_puzzlers}")

        # normalize the scores by giving the 4th highest best_three score a value of 100, and the rest of the scores are scaled accordingly
        if len(list_of_puzzlers) >= 4:
            fourth_highest_score = list_of_puzzlers[3][1]
        else:
            fourth_highest_score = list_of_puzzlers[-1][1]  
        
        for i, puzzler in enumerate(list_of_puzzlers):
            if fourth_highest_score > 0:
                normalized_score = (puzzler[1] / fourth_highest_score) * 100
            
            list_of_puzzlers[i][1] = round(normalized_score, 2) # update the best_three attribute of the Puzzler object
            #dict_Indian_puzzlers[name][2] = round(normalized_score, 2) # store the normalized score in the points list

        def print_normalized_scores():
            print(f"\nNormalized scores of Puzzlers:\n")
            for i in range(len(list_of_puzzlers)):
                name, best_three = list_of_puzzlers[i]
                country = 'IN' # since we are only considering Indian puzzlers
                points = best_three # get the normlized points   
                print(f"{name:<20} {country:<10} {points:>10.2f}")
        
        print_normalized_scores()
        
        

    # Steps 
    iterate_over_rankings() # only first 5 rounds
    sort_points()           # sort the points of each puzzler across rounds
    print_puzzlers()        # print the unique puzzlers across all rounds
    normalize_scores()      # take the best 3 scores of each puzzler, sum them up to make a best_three, and normalize the scores by giving the 4th highest best_three score a value of 100, and the rest of the scores are scaled accordingly. The normalized scores are stored in a new attribute of the Puzzler class called best_three.

    

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