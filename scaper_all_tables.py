# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 21:11:11 2021

@author: alindsey

Saves draws as dataframe csv.
"""

##############################################################################
# IMPORTS
##############################################################################
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


##############################################################################
# GLOBALS
##############################################################################
URL = ('https://www.canada.ca/en/immigration-refugees-citizenship/corporate/ma'
       'ndate/policies-operational-instructions-agreements/ministerial-instruc'
       'tions/express-entry-rounds.html#wb-auto-4')
PATH = 'data/all_draws.csv'


##############################################################################
# CLASSES
##############################################################################
class Draw:
    
    numDraws = 0
    
    def __init__(self, program, numInv, date, score):
        self.program = program
        self.numInv = numInv
        self.date = date
        self.score = score
        
        Draw.numDraws += 1


##############################################################################
# FUNCTIONS
##############################################################################
def getResponse(url):
    """
    Retrieves text from URL as html.
    """         
    print('Connecting...')
    response = requests.get(url).text
    print('Retrieved')
    
    return response


def tableScraper(response):
    """
    Gets table and adds each row as row in df.
    """
    print('Parsing...')
    soup = BeautifulSoup(response, 'lxml')
    
    print('Found table')
    htmlTable = soup.find('table')
    prevDraws = pd.read_html(str(htmlTable))[0]
    print('Table converted to df',
          '\n\nColumns:')
    for index, column in enumerate(prevDraws.columns):
        print('Column #{}: {}'.format(index, column))
        if index == len(prevDraws.columns) - 1:
            print()
    
    return prevDraws


def tableScraper_class(response):
    """
    Gets table and adds each row as a class.
    """
    print('Parsing...')
    soup = BeautifulSoup(response, 'lxml')
    
    print('Found table')
    htmlTable = soup.find('table')
    tableRows = htmlTable.find_all('tr')
    for i, row in enumerate(tableRows):
        print(i, row.text)



def saveTable(table, path='data/prevDraws.csv'):
    """
    Saves dataframe of previous draws to path.
    """
    print('Saving table as csv')
    table.to_csv(path)
    print('Table saved at {}'.format(path))



response = getResponse(URL)
table = tableScraper_class(response)
    
##############################################################################
# MAIN
##############################################################################
# def main():
#     while True:
#         response = getResponse(URL)
#         table = tableScraper_class(response)
#         # saveTable(table)
        
#         # sleep
#         print('Sleeping!\n\n')   
#         time.sleep(10)   


# ##############################################################################
# # RUNNER
# ##############################################################################
# if __name__ == '__main__':
#     main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    