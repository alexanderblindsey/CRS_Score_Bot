# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 22:26:13 2020

@author: alindsey
"""
import praw
import time
import pandas as pd
import config

PATH_DRAW = 'data/last_draw.csv'
MATCH_WORDS = ['!CRS?']
REPLY_TEST = 'Test Reply'
cache = set()


def reply(path=PATH_DRAW):
    """
    Fetches data and creates reply.
    """
    # fetch data & read into dataframe
    df = pd.read_csv(path, header=1, index_col=None)
    
    # program = df.iloc[1][1]
    # num_inv = df.iloc[2][1]
    draw_date = df.iloc[3][1]
    score = df.iloc[4][1]

    msg = ('Last Express Entry draw: {}\n'.format(draw_date) + 
           '\nMinimum CRS Score: {}'.format(score))    
    
    return msg


def authenticate():
    """
    Logs in to Reddit using account information from config file.
    """
    print('Authenticating...')
    reddit = praw.Reddit(username=config.username,
                         password=config.password,
                         client_id=config.client_id,
                         client_secret=config.client_secret,
                         user_agent="cunstitution's CRS score bot v0.1")
    print('Authenticated as {}.'.format(reddit.user.me()))
    return reddit


def main():
    while True:
        reddit = authenticate()
        to_reply = reply()
        run(reddit, cache, to_reply)
        
        # sleep
        print('Sleeping...')
        time.sleep(10)


def run(reddit, cache, reply, sub='test'):
    """
    Posts on Reddit if a comment with the right keyword is found.
    """
    subreddit = reddit.subreddit(sub)
    comments = subreddit.comments(limit=25)
    print('Searching for comments...')
    for comment in comments:
        comment_text = comment.body
        isMatch = any(string in comment_text for string in MATCH_WORDS)
        if isMatch and comment.id not in cache:
            print('Comment found!')
            comment.reply(reply)
            cache.add(comment.id)
            print('Replied')
        else:
            print('Skip')
            
    print('Done Searching \nCache: {}'.format(cache))


def replied_to(to_save=cache):
    """"
    Saves cache as csv. 
    """
    print('Saving as CSV')
    
    

if __name__ == '__main__':
    main()
