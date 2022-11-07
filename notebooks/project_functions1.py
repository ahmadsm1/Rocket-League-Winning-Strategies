from re import A
import pandas as pd
import numpy as np

def load_clean(path):
    """
    Cleans and appropriately modifies the raw dataset provided to it. Drops unnecessary columns and keep
    the ones needed.

    Arguments:
    path - (DataFrame) the raw data to clean
    """
    
    df = (
        pd.read_csv(path)
        .dropna()
        .drop(['team_slug', 'demo_taken', 'movement_count_powerslide', 'core_score', 'core_shooting_percentage', 'color', 'team_id'], axis=1)
        .rename(columns={'movement_time_high_air': 'air_time'})
        .rename(columns={'positioning_time_defensive_half': 'defense_time'})
        .rename(columns={'positioning_time_offensive_half': 'offense_time'})
        .filter(regex='^((?!positioning).)*$')
        .filter(regex='^((?!movement_time).)*$')
        .filter(regex='^((?!boost).)*$')
    )
    return df

def merge_dfs(df1, df2_path, on_key):
    """ 
    Merges the two databases together and drops duplicate rows.

    Arguments:
    df1 - (DataFrame) our original, main dataframe
    df2_path - (String) the path to the dataframe from which we need to append columns
    on_key - (String) the key which we will use to match each game to its appropriate data (match_id)
    """
    df2 = (
        pd.read_csv(df2_path)
        .filter(items=['match_id', 'event', 'event_split'])
        .drop_duplicates()
    )

    result = pd.merge(df1, df2, on=on_key)

    return result


def play_style_stats(df, mean_air_time):
    """
    Creates new column which shows whether a team had a ground or aerial playstyle.
    It determine this by checking if the time spent in the air by a team is greater than the average
    of all matches throughout the season. Returns winning teams only.

    The mean_air_time is a parameter and calculated outside of this function because it must remain constant,
    even when we will be comparing 2 different dataset (majors vs total). See notebook to understand.

    Arguments:
    df - (DataFrame) our main dataframe.
    mean_air_time - (double) average air time for comparison
    """
    q1 = df
    q1["playstyle"] = np.where(df['air_time'] >= mean_air_time, "air", "ground")
    ans = q1.query("winner")
    #ans1 = ans.filter(['event_split', 'event', 'playstyle'])
    return ans.filter(['event_split', 'event', 'playstyle', 'winner'])

def region_agg(df):
    """
    Creates new column to see if a match was played aggressively or passively. Our criteria here 
    for judging is whether a game had greater than average demolitions, shots made towards the net 
    and total distance travelled

    Arguments:
    df - (DataFrame) our main dataframe to examine the data from and add the column to.
    """
    
    q2 = df

    mean_demos = q2["demo_inflicted"].mean()
    mean_shots = q2["core_shots"].mean()
    mean_total_distance = q2["movement_total_distance"].mean()

    q2["agg_pass"] = np.where((q2['movement_total_distance'] >= mean_total_distance) & 
                                    (q2['core_shots'] >= mean_shots) & 
                                    (q2['demo_inflicted'] >= mean_demos), "aggressive", "passive")

    return q2

    # regions = ["Oceania", "North\nAmerica", "South\nAmerica", "Europe", "Middle\nEast", "Africa", "Asia\nNorth", "Asia\nSouth"]
    # agg_matches = [
    #     q2.query("agg_pass == 'aggressive' and team_region == 'Oceania'").shape[0],
    #     q2.query("agg_pass == 'aggressive' and team_region == 'North America'").shape[0],
    #     q2.query("agg_pass == 'aggressive' and team_region == 'South America'").shape[0],
    #     q2.query("agg_pass == 'aggressive' and team_region == 'Europe'").shape[0],
    #     q2.query("agg_pass == 'aggressive' and team_region == 'Middle East & North Africa'").shape[0],
    #     q2.query("agg_pass == 'aggressive' and team_region == 'Sub-Saharan Africa'").shape[0],
    #     q2.query("agg_pass == 'aggressive' and team_region == 'Asia-Pacific North'").shape[0],
    #     q2.query("agg_pass == 'aggressive' and team_region == 'Asia-Pacific South'").shape[0]]

    # agg_count = pd.DataFrame({"Regions":regions, "Matches":agg_matches})

    

# def good_goalkeeping(df):
#     q3 = df
#     mean_save_count = df["core_saves"].mean()

#     q3["good_gk"] = np.where(df['core_saves'] > mean_save_count, True, False)

#     winter_pc = q3.query("interesting and event_split == 'Winter'").shape[0]/q3.query("event_split == 'Winter'").shape[0]
#     fall_pc = q3.query("interesting and event_split == 'Fall'").shape[0]/q3.query("event_split == 'Fall'").shape[0]
#     spring_pc = q3.query("interesting and event_split == 'Spring'").shape[0]/q3.query("event_split == 'Spring'").shape[0]
#     summer_pc = q3.query("interesting and event_split == 'Summer'").shape[0]/q3.query("event_split == 'Summer'").shape[0]

#     event_splits = ['Fall', 'Winter', 'Spring', 'Summer']
#     percentages = [fall_pc, winter_pc, spring_pc, summer_pc]

#     data_plot = pd.DataFrame({"Event_splits":event_splits, "Percentages":percentages})

#     return q3