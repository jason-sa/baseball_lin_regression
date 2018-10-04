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

def build_rookie_pages(start, end, driver):
    rookie_pages = pd.DataFrame(columns=['year','link','html'])
    rookie_player_pages = pd.DataFrame(columns=['year','name','link','html'])
    
    #attempt to load from csv
    try:
        rookie_pages = pd.read_csv('data/rookie_pages.csv')
    except FileNotFoundError:
        pass
    print(rookie_pages.shape)
    try:
        rookie_player_pages = pd.read_csv('data/rookie_player_pages.csv')
    except FileNotFoundError:
        pass
    print(rookie_player_pages.shape)
    
    for i in range(start, end+1):
        links_list = []
        names_list = []
        
        #if year == i, then move onto link loop
        if not (rookie_pages.year == i).any():
            print('new rookie page data')
            url = 'https://www.baseball-reference.com/leagues/MLB/'+str(i)+'-rookies.shtml'
#             print('Scraping', url)
            driver.get(url)
            rookie_pages.loc[i] = [i, url, driver.page_source]

            # scrape the rookie batters (includes pitchers if PA)
            batting = driver.find_element_by_id('misc_batting') ## HTML tables
            links = batting.find_elements_by_xpath('.//tbody/tr/td/a') ## player pages

            # add these to the DF to save
            links_list = [a.get_attribute('href') for a in links if re.search(r'players/.', a.get_attribute('href'))]
            names_list = [a.text for a in links if re.search(r'players/.', a.get_attribute('href'))]

            rookie_pages.to_csv('data/rookie_pages.csv')
        
        if len(links_list) != 0: # add new data
            index = rookie_player_pages.index.max()+1
            index_l = list(range(index, index+len(links_list)+1))
            year_l = [i] * len(links_list)
            rookie_player_pages.loc[index_l] = [year_l, names_list, links_list, np.nan()]

        # loop only over incomplete data
#         index = rookier_player_pages.index.max() + 1
        
        for l in rookie_player_pages.loc[(rookie_player_pages.html == np.nan), 'link'].values;
            driver.get(l)
#             print(names_list[k])
            rookie_player_pages.loc[index, 'html'] = driver.page_source
            if index != 0 and index % 10 == 0:
                rookie_player_pages.to_csv('data/rookie_player_pages.csv')
            index += 1
        
        rookie_player_pages.to_csv('data/rookie_player_pages.csv')

    return rookie_pages, rookie_player_pages
