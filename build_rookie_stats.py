import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import re
import baseball as bb

PATH_S = '/Users/jadams/ds/metis/baseball_lin_regression/data/processed_df/salary.csv'
PATH_R = '/Users/jadams/ds/metis/baseball_lin_regression/data/processed_df/rookies.csv'
PATH_RS = '/Users/jadams/ds/metis/baseball_lin_regression/data/processed_df/rookie_stats.csv'
PATH_PLAYER_PAGES = '/Users/jadams/ds/metis/baseball_lin_regression/data/rookie_player_pages.csv'
PATH_PARTITION = '/Users/jadams/ds/metis/baseball_lin_regression/data/rookie_player_partition'

# df_stats_l = ([bb.build_rookie_year_df(pd.read_csv(f'data/rookie_player_partition/rookie_player_{i}.csv', index_col=0).reset_index())
                                    #   for i in range(11)])
# 
# df_stats = pd.concat(df_stats_l)
df = pd.read_csv('data/rookie_player_pages.csv', index_col=0)
df.reset_index(inplace=True)
df_stats = bb.build_rookie_year_df(df.iloc[:10])
df_stats.to_csv('data/processed_df/rookie_stats_2.csv')