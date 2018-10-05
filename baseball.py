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
import re


def get_player_data(soup_players, year, name):
    # Get position
    position = soup_players.find('p')
    position = position.contents[2].strip()
    
    if position in 'Pitcher':
        return None

    # Get batting stats
    batting = soup_players.find('table',{'id':'batting_standard'})

    batting_tbl_list = pd.read_html(str(batting))
    batting_df = batting_tbl_list[0]
    batting_df = batting_df[:-1]

    rookie_stats = batting_df[(batting_df.Year == str(year))]
    rookie_stats = rookie_stats[(~rookie_stats.Tm.str.contains('-min'))]
    rookie_stats = rookie_stats[rookie_stats.Tm != 'TOT']

    columns = ['Year', 'Age', 'Tm', 'Lg', 'G', 'PA', 'AB', 'R','H', 'SB','BA','HR','TB','2B','3B','RBI','BB','SO']
    rookie_stats = rookie_stats.loc[:, columns]  
    rookie_stats['position'] = position
    rookie_stats['name'] = name
    rookie_stats.Year = rookie_stats.Year.astype(int)

    return rookie_stats

def get_player_soup(ind, df):
    url = df.html[ind]
    return BeautifulSoup(url, 'lxml')

def build_rookie_year_df(pages):
    df = pd.DataFrame()
    for ind in pages.index:
        soup_players = get_player_soup(ind, pages)
        year = str(pages.year[ind])
        name = str(pages.name[ind])
    #     print(name, year, scrapped_rookie_players.link[ind])

        new_player = get_player_data(soup_players, year, name)
        if new_player is not None:
            df = df.append(new_player)
    
    return df

def build_rookie_table(rookie_pages):
    rookie_df = pd.DataFrame(columns=['Name','Debut','Age','Tm','rookie_year'])

    for i in rookie_pages.year.values:
        # scrape the rookie batters (includes pitchers if PA)
        soup_pages = BeautifulSoup(rookie_pages.html[i], 'lxml')
        batting = soup_pages.find('table',{'id':'misc_batting'})
        batting_df = pd.read_html(str(batting))
        
        # add Name, Debut, Age, Tm, and rookie_year
        year_df = batting_df[0].loc[:,['Name','Debut','Age','Tm']]
        year_df['rookie_year'] = [i] * batting_df[0].shape[0]
        year_df.rookie_year = year_df.rookie_year.astype(int)
        rookie_df = rookie_df.append(year_df)
        
        # Strip HOF indicator from name
        rookie_df.Name = rookie_df.Name.str.replace('HOF','')
        rookie_df[rookie_df.Name.str.contains('HOF')]
        rookie_df.Name = rookie_df.Name.str.strip()
       
    return rookie_df

def get_player_salary(ind, df, name):
    salary_soup = get_player_soup(ind, df)

    salary_html = salary_soup.find('table',{'id':'br-salaries'})
    if salary_html is None:
        return None    
    
    salary_tables_lst = pd.read_html(str(salary_html))
    salary_df = salary_tables_lst[0]
    
    salary_df = salary_df[~salary_df.Year.isnull()]
    salary_df = salary_df[salary_df.Year.str.contains(r'[1-2]\d{3}$')]

    salary_df['name'] = [name] * salary_df.shape[0]
    salary_df['UID'] = [ind] * salary_df.shape[0]
    
    return salary_df

def load_salary_data(players):
    dfs = [get_player_salary(ind, players, players.name[ind]) for ind in players.index]
    df = pd.concat(dfs)

    df.Salary = (df.Salary
                       .str.replace('$','')
                       .str.replace(',','')
                       .str.replace('*','')
                       )
    df.loc[df.Salary == '', 'Salary'] = np.nan
    df.Salary = df.Salary.astype(float)

    df.Age = df.Age.astype(float)

    df.loc[df.SrvTm == '?','SrvTm'] = np.nan
    df.SrvTm = df.SrvTm.astype(float)

        
    return df