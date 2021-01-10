# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 23:19:15 2021

@author: alindsey

For SQLite db.
"""

##############################################################################
# IMPORTS
##############################################################################
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd


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
# class Draw:
    
#     numDraws = 0
    
#     def __init__(self, program, num_inv, date, score):
#         self.program = program
#         self.num_inv = num_inv
#         self.date = date
#         self.score = score
        
#         Draw.numDraws += 1


##############################################################################
# FUNCTIONS
##############################################################################
def get_response(url):
    """
    Retrieves text from URL as html.
    """         
    print('Connecting...')
    response = requests.get(url).text
    print('Retrieved')
    
    return response


def table_scraper(response):
    """
    Gets table and adds each row.
    """
    print('Parsing...')
    soup = BeautifulSoup(response, 'lxml')
    
    print('Found table')
    html_table = soup.find('table')
    table_rows = html_table.find_all('tr')
    
    df = pd.DataFrame()
    
    for i, row in enumerate(table_rows):
        table_entries = row.find_all('td')
        
        for i_, entry in enumerate(table_entries):
            entry = entry.text
            print(i, i_, entry)
            
            if i_ == 0:
                df.at[i, 'draw_number'] = entry
                
            elif i_ == 1:
                df[i, 'draw_date'] = entry
            
            elif i_ == 2:
                df.at[i, 'program'] = entry
            
            elif i_ == 3:
                df.at[i, 'number_invited'] = entry
                
            elif i_ == 4:
                df.at[i, 'score'] = entry
                
            else:
                continue
            
       
        
        if i == 20:
            break
        print(df)
        print(df.columns)
        



response = get_response(URL)
table = table_scraper(response)
    
##############################################################################
# MAIN
##############################################################################
# def main():
#     while True:
#         response = getResponse(URL)
#         table = tableScraper(response)
#         # saveTable(table)
        
#         # sleep
#         print('Sleeping!\n\n')   
#         time.sleep(10)   


# ##############################################################################
# # RUNNER
# ##############################################################################
# if __name__ == '__main__':
#     main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    