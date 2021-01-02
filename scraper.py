# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 17:49:02 2020

@author: alindsey

Scrapes Immigration Canada website for details of last Express Entry draw.
"""

##############################################################################
# IMPORTS
##############################################################################
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime, timezone
import pandas as pd


##############################################################################
# GLOBALS
##############################################################################
URL = ('https://www.canada.ca/en/immigration-refugees-citizenship/services/im'
       'migrate-canada/express-entry/submit-profile/rounds-invitations.html')
PATH = 'data/last_draw.csv'


def get_response(url):
    """
    Connects to url.
    """         
    print('Connecting...')
    response = requests.get(url).text
    print('Retrieved')
    return response


def save_results(to_save, path=PATH):
    """
    Save results from scrape() as csv. 
    """
    print('Saving as CSV')    
    to_save.to_csv(path)
    print('Saved')  


def scrape(response):
    """
    Scrapes Immigration Canada website and finds relevant data.
    """
    print('Parsing...')
    class_ = 'mwsgeneric-base-html parbase section'
    soup = BeautifulSoup(response, 'lxml')
    container = soup.find('html').main
    body_text = container.find_all('div', class_=class_)[1]
    last_round = body_text.find_all('div', class_=class_)[1]   
    paras = last_round.find_all('p')
    
    print('Relevant data found')
    
    program = paras[1].text
    num_inv = paras[3].text.split(':')[1].split('a')[0].split('F')[0].lstrip()
    draw_date = paras[5].text.split(':')[1].split('at')[0].lstrip().rstrip()
    score = paras[6].text.split(':')[1].lstrip()
    
    print('Program: {}\nnum_inv: {}\ndate: {}\nscore: {}'.format(program,
                                                                 num_inv,
                                                                 draw_date,
                                                                 score))
    accessed = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    last_draw = pd.Series({'variable':'value',
                           'accessed':accessed,
                           'program':program,
                           'num_inv':num_inv,
                           'draw_date':draw_date,
                           'score':score})
    print('Scraped at: {}'.format(accessed))

    return last_draw


##############################################################################
# MAIN
##############################################################################
def main():
    while True:
        site_text = scrape(get_response(URL))
        save_results(site_text)
        
        # sleep
        print('Sleeping!\n\n')   
        time.sleep(10)   


##############################################################################
# RUNNER
##############################################################################
if __name__ == '__main__':
    main()