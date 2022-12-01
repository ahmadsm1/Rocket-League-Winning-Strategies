import pandas as pd
import numpy as np

def load_and_process(path):                 
    """
    Method Chain 1 (Load data, read the data, rename columns and drop rows with missing data)
    Arguments:
    path - raw data to process
    """
    
    df1 = (
        pd.read_csv(path)
        .rename(columns = {
            'team_name':'Team Name',
            'team_region':'Team Region',
            'core_shots':'Shots',
            # 'core_goals':'Goals',
            'core_saves':'Saves',
            'core_assists':'Assists',
            'boost_time_full_boost':'Time at Full Boost',
            'movement_total_distance':'Total Distance Moved',
            'movement_time_supersonic_speed':'Time at Supersonic Speed',
            'movement_time_high_air':'Time in High Air',
            'movement_count_powerslide':'Powerslide Distance',
            # 'demo_inflicted':'Demos Inflicted',
            'demo_taken':'Demos Taken',
            'score':'Score',
            'winner':'Winner',
            'DemosPerGoal':'Demos Per Goal'
        })
        .dropna(how='any',axis=0)
          )
    """
    Method Chain 2 (Create new columns, drop others, and do processing)
    """
    df2 = (
        df1
        .assign(DemosPerGoal=lambda x: x.demo_inflicted / x.core_goals)
        .drop(columns = [
            'match_id',
            'team_id',
            'team_slug',
            'color',
            'positioning_time_neutral_third',
            'positioning_time_offensive_third',
            'positioning_time_defensive_half',
            'positioning_time_offensive_half',
            'movement_time_powerslide',
            'positioning_time_defensive_third',
            'positioning_time_behind_ball',
            'positioning_time_in_front_ball',
            'movement_time_slow_speed',
            'movement_time_ground',
            'movement_time_low_air',
            'boost_time_boost_75_100',
            'core_score',
            'core_shooting_percentage',
            'movement_time_boost_speed',
            'boost_amount_stolen_big',
            'boost_amount_stolen_small',
            'boost_amount_collected_small',
            'boost_amount_stolen',
            'boost_bpm',
            'boost_bcpm',
            'boost_avg_amount',
            'boost_amount_collected',
            'boost_count_collected_big',
            'boost_count_collected_small',
            'boost_count_stolen_small',
            'boost_count_stolen_big',
            'boost_amount_collected_big',
            'boost_amount_overfill',
            'boost_amount_overfill_stolen',
            'boost_amount_used_while_supersonic',
            'boost_time_boost_0_25',
            'boost_time_boost_25_50',
            'boost_time_boost_50_75',
            'boost_time_zero_boost'])
        .rename(columns = {
            'core_goals':'Goals',
            'demo_inflicted':'Demos Inflicted',
            'DemosPerGoal':'Demos Per Goal'})
      )

    # Return the latest dataframe

    return df2 