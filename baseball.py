import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time
import os
from selenium.webdriver.common.by import By
import pickle

def get_boxscore_urls(driver):
    urls = []
    links = driver.find_elements_by_link_text('Boxscore')
    for l in links:
        urls.append(l.get_attribute('href'))
    return urls

def write_pkl(data, name):
    with open('pickles/'+name+'.pkl', 'wb') as picklefile:
        pickle.dump(data, picklefile)

def build_rookie_table(start, end, driver):
#     urls = []
    rookie_df = pd.DataFrame(columns=['Name','Debut','Age','Tm','rookie_year'])
    for i in range(start, end+1):
#         urls.append('https://www.baseball-reference.com/leagues/MLB/'+str(i)+'-rookies.shtml')
        url = 'https://www.baseball-reference.com/leagues/MLB/'+str(i)+'-rookies.shtml'
        print('Scraping', url)
        driver.get(url)

        batting = driver.find_element_by_id('misc_batting')
        batting_df = pd.read_html(batting.get_attribute('outerHTML'))
        
        year_df = batting_df[0].loc[:,['Name','Debut','Age','Tm']]
        year_df['rookie_year'] = [i] * batting_df[0].shape[0]
#         print(year_df.head())
        rookie_df = rookie_df.append(year_df)
#         rookie_df.head()        
    return rookie_df 
