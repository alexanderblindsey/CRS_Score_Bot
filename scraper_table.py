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
import pandas as pd
import mysql.connector
from datetime import datetime, timezone
import config

##############################################################################
# GLOBALS
##############################################################################
URL = ('https://www.canada.ca/en/immigration-refugees-citizenship/corporate/ma'
       'ndate/policies-operational-instructions-agreements/ministerial-instruc'
       'tions/express-entry-rounds.html#wb-auto-4')


##############################################################################
# CLASSES
##############################################################################



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


def scrape(response):
    """
    Extracts data from the table on the IRCC website of all Express Entry
    draws. Stores this data as a dataframe.
    """
    print('Parsing...')
    soup = BeautifulSoup(response, 'lxml')
    html_table = soup.find('table')
    table_rows = html_table.find_all('tr')
    print('Found table')    
    
    draw_df = pd.DataFrame(columns=['draw_num',
                                    'draw_date',
                                    'program',
                                    'num_inv',
                                    'score'])
    
    print('Extracting info')
    for num_row, row in enumerate(table_rows):
        table_entries = row.find_all('td')
        draw_dict = {}
        
        for num_entry, entry in enumerate(table_entries):
            entry = entry.text            
            
            if num_entry == 0:
                draw_dict['draw_num'] = entry
                
            elif num_entry == 1:
                draw_dict['draw_date'] = entry
            
            elif num_entry == 2:
                draw_dict['program'] = entry
            
            elif num_entry == 3:
                draw_dict['num_inv'] = entry
                
            elif num_entry == 4:
                draw_dict['score'] = entry
                
            elif num_entry == 5: # num_entry 5 and 6 include redundant info
                draw_df = draw_df.append(draw_dict, ignore_index=True)
                draw_dict = {}
        
            else:
                continue
   
    print('Parsed - stored as df')
    return draw_df
        

def populate_db(df):    
    """
    Uses dataframe containing data on Express Entry draws to populate the 
    remote appropriate MySQL database table only if is empty.
    """
    config.gcp_server['database'] = 'bot_db'
    
    print('Establishing connection...')
    conn = mysql.connector.connect(**config.gcp_server)
    cursor = conn.cursor()
    print('Connection established')
    
    print('Checking if data in table')
    cursor.execute('SELECT EXISTS (SELECT 1 FROM Draws);')
    check_data = cursor.fetchall()   
    if 1 in check_data[0]:
        print('Data found')
    
    else:
        print('No data found', '\nPopulating table...')        
        df['created_at'] = ''
        
        for i in df.index:
            current_draw_num = int(df.at[i, 'draw_num'])
            current_draw_date = df.at[i, 'draw_date']
            current_program =  df.at[i, 'program']
            current_num_inv = int(df.at[i, 'num_inv'])
            current_score = int(df.at[i, 'score'])
            current_created_at = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            
            to_insert = (current_draw_num, 
                          current_draw_date,
                          current_program,
                          current_num_inv,
                          current_score,
                          current_created_at)
            
            query = ('INSERT INTO Draws (draw_num, draw_date, program, num_inv'
                      ', score, created_at) VALUES {}'.format(to_insert))

            cursor.execute(query)
            conn.commit()
            
        print('Table populated')
        
    print('Closing connection')
    conn.close()
    print('Connection closed')
        
        
def update_db(df):
    """
    Updates database with new draws.
    """
    config.gcp_server['database'] = 'bot_db'
    
    print('Establishing connection...')
    conn = mysql.connector.connect(**config.gcp_server)
    cursor = conn.cursor()
    print('Connection established')
    
    print('Checking if draw in db...')
    query = ('SELECT draw_num FROM Draws WHERE draw_num = (SELECT MAX (draw_num) FROM Draws)')
    
    last_draw_num = cursor.execute(query)
    
    
    
    

    
response = get_response(URL)
table = scrape(response)
populate_db(table)
    
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    