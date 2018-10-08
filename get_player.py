import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import requests
import time
import os
from selenium.webdriver.common.by import By
import pickle
import re

import time

def get_rookie_player_pages_html(rookie_player_pages, driver, stop=None):
    index = 0
    html_df = rookie_player_pages[rookie_player_pages.html.isnull()]

    for l in html_df.link.values:
        start = time.time()

        driver.get(l) #Could add try and except to write to csv if error, so can restart from last write. 

        end = time.time()
        print((end-start), l)
        rookie_player_pages.loc[rookie_player_pages.link == l, 'html'] = driver.page_source

        if index != 0 and index % 100 == 0:
            print('Rows completed', rookie_player_pages[~rookie_player_pages.html.isnull()].shape[0])
            rookie_player_pages.to_csv('data/rookie_player_pages.csv')

        if index == stop:
            break
        
        index += 1

    rookie_player_pages.to_csv('data/rookie_player_pages.csv')
    return rookie_player_pages

def build_rookie_pages(start, end, driver):
    rookie_pages = pd.DataFrame(columns=['year','link','html'])
    rookie_player_pages = pd.DataFrame(columns=['year','name','link','html'])
    
    #attempt to load from csv
    try:
        rookie_pages = pd.read_csv('data/rookie_pages.csv', index_col=0)
    except FileNotFoundError:
        pass
    print(rookie_pages.shape)
    try:
        rookie_player_pages = pd.read_csv('data/rookie_player_pages.csv', index_col=0)
    except FileNotFoundError:
        pass
    print(rookie_player_pages.shape)
    
    for i in range(start, end+1):
        links_list = []
        names_list = []
        
        #if year == i, then move onto link loop
        if not (rookie_pages.year == i).any():
            url = 'https://www.baseball-reference.com/leagues/MLB/'+str(i)+'-rookies.shtml'
            start = time.time()
            driver.get(url)
            end = time.time()
            print(end-start, i)
            rookie_pages.loc[i] = [i, url, driver.page_source]

            # scrape the rookie batters (includes pitchers if PA)
            batting = driver.find_element_by_id('misc_batting') ## HTML tables
            links = batting.find_elements_by_xpath('.//tbody/tr/td/a') ## player pages

            # add these to the DF to save
            links_list = [a.get_attribute('href') for a in links if re.search(r'players/.', a.get_attribute('href'))]
            names_list = [a.text for a in links if re.search(r'players/.', a.get_attribute('href'))]


        
        if len(links_list) != 0: # add new data
#             index = rookie_player_pages.index.max()+1
#             index_l = list(range(index, index+len(links_list)))
            year_l = [i] * len(links_list)
            new_df = pd.DataFrame({'year': year_l, 'name': names_list, 'link': links_list})
            rookie_player_pages = rookie_player_pages.append(new_df, sort=True)
        
        rookie_pages.to_csv('data/rookie_pages.csv')
        rookie_player_pages.to_csv('data/rookie_player_pages.csv')

    return rookie_pages, rookie_player_pages

chromedriver = "chromedriver" # path to the chromedriver executable
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

# while True:
#     try:
#         rookie_pages, rookie_player_pages = build_rookie_pages(1985, 2017, driver)
#     except TimeoutException:
#         pass
#     else:
#         break

tries = 0
while tries <= 2:
    try:
        rookie_player_pages = pd.read_csv('data/rookie_player_pages.csv',index_col=0)
        print('Try:', tries)
        print(rookie_player_pages.shape)
        rookie_player_pages = get_rookie_player_pages_html(rookie_player_pages, driver, stop=6000)
    except TimeoutException:
        tries += 1
        pass
    else:
        break
driver.close()