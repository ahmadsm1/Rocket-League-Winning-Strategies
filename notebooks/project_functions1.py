import pandas as pd
import numpy as np

def load_clean(path):

    # Method 1: load and deal with missing data
    df = (
        pd.read_csv(path)
        .dropna()
        .drop(['team_slug', 'demo_taken', 'movement_count_powerslide', 'core_score', 'core_shooting_percentage', 'color', 'team_id'], axis=1)
        .rename(columns={'movement_time_high_air': 'air_time'})
        .filter(regex='^((?!positioning).)*$')
        .filter(regex='^((?!movement_time).)*$')
        .filter(regex='^((?!boost).)*$')
    )
    return df

#load_process('../data/raw/matches_by_teams.csv')