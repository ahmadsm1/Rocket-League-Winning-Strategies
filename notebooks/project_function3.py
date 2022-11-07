
import pandas as pd
import numpy as np

def load_clean(path):
    "cleans and removes columns that arent needed"
    df = (
        pd.read_csv(path)
        .dropna()
        .drop(['team_slug','positioning_time_behind_ball','positioning_time_in_front_ball', 'demo_inflicted','demo_taken','movement_count_powerslide', 'core_shooting_percentage', 'color', 'team_id'
'positioning_time_defensive_third', 'positioning_time_neutral_third','positioning_time_offensive_third',], axis=1)
        .rename(columns={'positioning_time_defensive_half': 'defense_time'})
        .rename(columns={'positioning_time_offensive_half': 'offense_time'})
        .filter(regex='^((?!boost).)*$')
    )
    return df

def merge_dfs(df1,df2_path, on_key):
    "Lets merge the main and match_by_teams files"
    df2 = (
        pd.read_csv(df2_path)
        .filter(items=['match_id', 'event', 'event_split'])
        .drop_duplicates()
    )

    result = pd.merge(df1, df2, on=on_key)

    return result

def play_stats(df, mean_defense_time):
    
    q1 = df
    q1["playstyle"] = np.where(df['defense_time'] >= mean_defense_time, "defense", "offense")
    ans = q1.query("winner")
    #ans1 = ans.filter(['event_split', 'event', 'playstyle'])
    return ans.filter(['event_split', 'event', 'playstyle', 'winner'])
def boost_stats(df, mean_boost_time):
    q1 = df
    q1["playstyle"] = np.where(df['boost_bcpm'] >= mean_boost_time, "boost", "goals")
    ans = q1.query("winner")
    #ans1 = ans.filter(['event_split', 'event', 'playstyle'])
    return ans.filter(['event_split', 'event', 'playstyle', 'winner'])