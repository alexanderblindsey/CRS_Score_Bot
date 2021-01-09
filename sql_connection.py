# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 20:14:03 2021

@author: alindsey
"""

import mysql.connector
import config


config.gcp_server['database'] = 'crs_score_bot'

cnxn = mysql.connector.connect(**config.gcp_server)

cursor = cnxn.cursor()