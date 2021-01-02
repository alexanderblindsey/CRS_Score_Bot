# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 22:26:13 2020

@author: alindsey
"""

##############################################################################
# IMPORTS
##############################################################################
import praw
import time
import pandas as pd
import os.path
from datetime import datetime, timezone
import config

##############################################################################
# GLOBALS
##############################################################################
PATH_DRAW = 'data/last_draw.csv'
PATH_CACHE = 'data/cache.csv'
MATCH_WORDS = ['!CRS']
REPLY_TEST = 'Test Reply'

##############################################################################
# FUNCTIONS
##############################################################################
def authenticate():
    """
    Authenticates account using account information from config.py file.
    """
    print('Authenticating...')
    reddit = praw.Reddit(username=config.username,
                         password=config.password,
                         client_id=config.client_id,
                         client_secret=config.client_secret,
                         user_agent="cunstitution's CRS score bot v0.1")
    print('Authenticated as {}.\n'.format(reddit.user.me()) + 
          'Accessed: {}'.format(datetime
                                .now(timezone.utc)
                                .strftime('%Y-%m-%d %H:%M:%S')))
    
    return reddit


def get_cache(path_=PATH_CACHE):
    """"
    If cache does not exist, it creates one. Otherwise, it loads the 
    cache into memory.
    """
    print('Searching for cache...')
    if os.path.exists(path_)==True:
        print('Cache exists')
        cache = pd.read_csv(path_, squeeze=True) 
        print('Cache with {} entries loaded'.format(len(cache)))
        
    else:
        print('Cache does not exist')
        cache = pd.Series(['test1', 'test2'], dtype=str)
        print('Cache created')
    
    return cache


def reply(path_=PATH_DRAW):
    """
    Fetches CRS data from the csv and generates the bot's reply message.
    """
    df = pd.read_csv(path_, header=1, index_col=None)
    
    # program = df.iloc[1][1]
    # num_inv = df.iloc[2][1]
    draw_date = df.iloc[3][1]
    score = df.iloc[4][1]

    msg = ('Last Express Entry draw: {}\n'.format(draw_date) + 
           '\nMinimum CRS Score: {}'.format(score))    
    
    return msg


def run(reddit, reply, cache, sub='test'):
    """
    Posts on the specified subreddit if a comment containing a keyword 
    is found. Updates cache in memory.
    """
    subreddit = reddit.subreddit(sub)
    comments = subreddit.comments(limit=25)
    
    print('Searching for comments...')
    
    for comment in comments:
        comment_text = comment.body
        isMatch = any(string in comment_text for string in MATCH_WORDS)
        if isMatch and comment.id not in cache.values:
            print('Comment found!')
            # comment.reply(reply)
            print('Replied!')
            cache = cache.append(pd.Series([comment.id], dtype=str),
                                 ignore_index=True)      
            print('{} added to cache'.format(comment.id))

        else:
            print('Skip')
            
    print('Done Searching \nCache:\n {}'.format(cache))
    
    return cache

    
def update_cache(cache, path_=PATH_CACHE):
    """
    Saves cache as csv to same path as it was loaded in from, replacing the
    csv file.
    """
    cache.to_csv(path_, index=False)
    print('Cache saved as csv')

##############################################################################
# MAIN    
##############################################################################
def main():
    while True:
        cache = get_cache()
        reddit = authenticate()
        to_reply = reply()
        
        runner = run(reddit, to_reply, cache)
        update_cache(runner)

        # sleep
        print('Sleeping...\n\n')
        time.sleep(10)

##############################################################################
# RUNNER
##############################################################################
if __name__ == '__main__':
    main()