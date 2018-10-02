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
