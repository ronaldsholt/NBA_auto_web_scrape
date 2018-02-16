#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 13:22:38 2018

@author: RSH
"""

from bs4 import BeautifulSoup as bs
import urllib
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import os.path

current_directory = '/Users/kra7830/NBA_NN_DK/data_folder/'
#final_directory = os.path.join(current_directory, r'data_folder')
#if not os.path.exists(final_directory):
 #   os.makedirs(final_directory)


base_url = "https://www.fantasycruncher.com/lineup-rewind/draftkings/NBA/DATE"

driver = webdriver.Chrome('/Users/kra7830/Desktop/chromedriver')

from datetime import timedelta, date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

#insert date range here
start_date = date(2017, 12, 25)
end_date = date(2018, 2, 4)

for single_date in daterange(start_date, end_date):
    print single_date.strftime("%Y-%m-%d") #gives the proper date format
    
    #new_dates = base_url.replace("DATE", single_date.strftime("%Y-%m-%d")) #inserts into the DATE of the url 
    driver.get(base_url.replace("DATE", single_date.strftime("%Y-%m-%d")))
    #driver.get(new_dates)
    
### A pop-up will appear and suggest for you to close it ###
    close_login = driver.find_element_by_class_name("close-login-alert")
    close_login.click()
    
### we need to gather all players from the drop down...
## Use dev tools in chrome; find element name and find value to select... 
# then run code below
    select = Select(driver.find_element_by_name('ff_length'))
    select.select_by_value('-1')
    
### This code "clicks" copy player list - this copies player data to the os clipboard
    elem1 = driver.find_element_by_link_text("copy player list")
    elem1.click()
    
### Closes pop-up that confirms copied player list
    close_copy = driver.find_element_by_class_name("sa-confirm-button-container")
    close_copy.click()

### Pandas reads clipboard, converts to DF, then exports to CSV... 
    df2 = pd.read_clipboard()
    df2.to_csv(current_directory + single_date.strftime("%Y-%m-%d"))
    #df2.to_csv(single_date.strftime("%Y-%m-%d"), path='/Users/kra7830/NBA_NN_DK/data_folder/')
    
    
########### Build One Data file #################
    
#df = pd.read_csv(current_directory + '2017-11-25', skiprows=[0], header=None)
df = pd.read_csv(current_directory + '2017-11-25')
 
col_names = df.columns    
    
import glob
path = current_directory                   # use your path
all_files = glob.glob(os.path.join(path, "*"))     # advisable to use os.path.join as this makes concatenation OS independent

df_from_each_file = (pd.read_csv(f, skiprows=[0], header=None) for f in all_files)
concatenated_df = pd.concat(df_from_each_file, ignore_index=True)    
    
concatenated_df.columns = col_names    
    
concatenated_df.to_csv('combined_nba_data.csv')  
    
    
    
    
    
    
    
    
    
