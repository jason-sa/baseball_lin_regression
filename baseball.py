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
import time
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import RidgeCV
from sklearn.linear_model import LassoCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
import scipy.stats as stats

PATH_RS = '/Users/jadams/ds/metis/baseball_lin_regression/data/processed_df/rookie_stats.csv'
PATH_S = '/Users/jadams/ds/metis/baseball_lin_regression/data/processed_df/salary.csv'

def count_awards(s):    
    awards = 0
    s = str(s)
    if len(s) > 0:
        awards = s.count(',')+1
    return awards

def get_player_data(html, year, name):
    soup_players = BeautifulSoup(html, 'lxml')

    # Get position
    position = soup_players.find('p')
    position = position.contents[2].strip()
    
    if position in 'Pitcher':
        return None

    # Get the debut for identification in case duplicate name
    debut = soup_players.find('a', {'href': re.compile('=debut')})
    debut = debut.contents

    # Get batting stats
    batting = soup_players.find('table',{'id':'batting_standard'})

    batting_tbl_list = pd.read_html(str(batting))
    batting_df = batting_tbl_list[0]
    batting_df = batting_df[:-1]

    rookie_stats = batting_df[(batting_df.Year == str(year))]
    rookie_stats = rookie_stats[(~rookie_stats.Tm.str.contains('-min'))]
    rookie_stats = rookie_stats[rookie_stats.Tm != 'TOT']

    columns = ['Year', 'Age', 'Tm', 'Lg', 'G', 'PA', 'AB', 'R','H', 'SB','BA','HR','TB','2B','3B','RBI','BB','SO','Awards']
    rookie_stats = rookie_stats.loc[:, columns]
    rookie_stats = rookie_stats[rookie_stats.Lg.str.contains(r'[A,N]L$')]  
    rookie_stats['position'] = position
    rookie_stats['name'] = name
    rookie_stats['debut'] = debut * rookie_stats.shape[0]

    rookie_stats.Year = rookie_stats.Year.astype(int)
    rookie_stats.debut = pd.to_datetime(rookie_stats.debut, format='%B %d, %Y')

    rookie_stats.loc[rookie_stats.Awards.isnull(),'Awards'] = ''
    rookie_stats['award_count'] = rookie_stats.Awards.apply(count_awards)

    with open(PATH_RS, 'a') as f:
        rookie_stats.to_csv(f, header=False)

    # return rookie_stats

def get_player_soup(ind, df):
    url = df.html[ind]
    return BeautifulSoup(url, 'lxml')

def build_rookie_table(rookie_pages):
    rookie_df = pd.DataFrame(columns=['Name','Debut','Age','Tm','rookie_year'])
    rookie_dfs = []

    for i in rookie_pages.year.values:
        # scrape the rookie batters (includes pitchers if PA)
        soup_pages = BeautifulSoup(rookie_pages.html[i], 'lxml')
        batting = soup_pages.find('table',{'id':'misc_batting'})
        batting_df = pd.read_html(str(batting))
        
        # add Name, Debut, Age, Tm, and rookie_year
        year_df = batting_df[0].loc[:,['Name','Debut','Age','Tm']]
        year_df['rookie_year'] = [i] * batting_df[0].shape[0]
        year_df.rookie_year = year_df.rookie_year.astype(int)
        rookie_dfs.append(year_df) #= rookie_df.append(year_df)
        
    # Combine the rookie_dfs
    rookie_df = pd.concat(rookie_dfs)

    # Strip HOF indicator from name
    rookie_df.Name = rookie_df.Name.str.replace('HOF','')
    rookie_df[rookie_df.Name.str.contains('HOF')]
    rookie_df.Name = rookie_df.Name.str.strip()

    # Make Debut a date time
    rookie_df.Debut = rookie_df.Debut.astype('datetime64')
       
    return rookie_df

def get_player_salary(html, year, name, ind):
    salary_soup = BeautifulSoup(html, 'lxml')

    salary_html = salary_soup.find('table',{'id':'br-salaries'})
    if salary_html is None:
        return None    
    
    salary_tables_lst = pd.read_html(str(salary_html))
    salary_df = salary_tables_lst[0]
    
    salary_df = salary_df[~salary_df.Year.isnull()]
    salary_df = salary_df[salary_df.Year.str.contains(r'[1-2]\d{3}$')]

    salary_df['name'] = [name] * salary_df.shape[0]
    salary_df['UID'] = [ind] * salary_df.shape[0]
    salary_df['rookie_year'] = [year] * salary_df.shape[0]

    salary_df.Salary = (salary_df.Salary
                    .str.replace('$','')
                    .str.replace(',','')
                    .str.replace('*','')
                    )
    salary_df.loc[salary_df.Salary == '', 'Salary'] = np.nan
    salary_df.Salary = salary_df.Salary.astype(float)

    salary_df.Age = salary_df.Age.astype(float)

    if salary_df.SrvTm.dtype != 'float64':
        salary_df.loc[salary_df.SrvTm == '?','SrvTm'] = np.nan
        salary_df.SrvTm = salary_df.SrvTm.astype(float)

    if ind == 1:
        salary_df.to_csv(PATH_S)
    else:
        with open(PATH_S, 'a') as f:
            salary_df.to_csv(f, header=False)

def partion_rookie_players(size, df, name):
    tot = df.shape[0]

    i = 0
    while i <= tot:
        df.iloc[i:i+size].to_pickle('data/pickles/'+ name + '_' + str(i//size) + '.pkl')
    i += size

def run_models(X_train, y_train, name, results = None, cv=10, alphas=np.logspace(-3, -0.5, 10)):
    ''' Method to quickly run all models with different feature sets X_train
    '''    
    # capture the results for the feature set
    model_results = pd.Series(name=name)

    # Perform 10-fold cross-validation linear regression model.

    lin_model = LinearRegression()
    scores = cross_val_score(lin_model, X_train, y_train, cv=cv, scoring='neg_mean_squared_error')
    model_results['linear model - cv10'] = np.mean(-scores)
    # model_results

    # Build a Lasso model with standard scaling.

    # Now perform a 10-fold cross validation for same range of alphas.

    # probably want to change this range based on GridCV
    # alphas = [10**a for a in range(-2,5)]

    cv_lasso = make_pipeline(StandardScaler(), LassoCV(cv=cv, alphas=alphas, tol=0.001))
    cv_lasso.fit(X_train, y_train)
    model_results['lasso cv - ' + str(cv_lasso.get_params()['lassocv'].alpha_)] = mean_mse_Lasso(cv_lasso, 'lassocv')
    # model_results.sort_values()

    # Now 2-5 degree polynomial features and perform a 10-fold cross validation.

    for degrees in range(2,6):
        cv_lasso_poly = make_pipeline(PolynomialFeatures(degrees), StandardScaler(), LassoCV(cv=cv, alphas=alphas,tol=0.001))
        cv_lasso_poly.fit(X_train, y_train)
        model_results['lasso poly ' + str(degrees) + ' cv - ' + str(cv_lasso_poly.get_params()['lassocv'].alpha_)] = mean_mse_Lasso(cv_lasso_poly, 'lassocv')

    # model_results.sort_values()
    
    if results is None:
        results = pd.DataFrame(model_results)
    else:
        results = pd.concat([results, pd.DataFrame(model_results)], axis=1, sort=True)
        
    return results

def mean_mse_Lasso(model,name):
    mse = model.get_params()[name].mse_path_
    alphas = model.get_params()[name].alphas_
    mse_df = pd.DataFrame(data=mse, index=alphas)
    return mse_df.loc[model.get_params()[name].alpha_].mean()