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

        new_player = bb.get_player_data(soup_players, year, name)
        if new_player is not None:
            df = df.append(new_player)
    
    return df