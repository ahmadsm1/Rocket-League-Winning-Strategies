import pandas as pd
import numpy as np

df = pd.read_csv('../data/raw/matches_by_teams.csv')

#Removing missing data
df = df.dropna()

#Removing unwanted columns
df = df.drop(['team_slug', 'demo_taken', 'movement_count_powerslide', 'core_score', 'core_shooting_percentage', 'color', 'team_id'], axis=1)
df = df[df.columns.drop(list(df.filter(regex='positioning*')))]
df = df.rename(columns={'movement_time_high_air': 'air_time'})
df = df[df.columns.drop(list(df.filter(regex='movement_time*')))]
df = df[df.columns.drop(list(df.filter(regex='boost*')))]

df

#################

# Data for Q1
mean_air_time = df["air_time"].mean()

# Data for Q2
mean_demos = df["demo_inflicted"].mean()
mean_shots = df["core_shots"].mean()
mean_total_distance = df["movement_total_distance"].mean()

# Data for Q3
mean_save_count = df["core_saves"].mean()

# Data for Q4
mean_assists = df["core_assists"].mean()

#####################

#Importing Regional and Splits
df2 = pd.read_csv('../data/raw/main.csv')[['match_id', 'event', 'event_split']].drop_duplicates()
result = pd.merge(df , df2 , on='match_id')

####################

# QUESTION 1: What play styles (ground, aerial) have higher chances to win a game?
# ANSWER: Staying on the ground is the more successful strategy overall, but at the higher levels of competition 
# (majors & world championship) aerial based plays are more successful. This could be because of the greater skill of players.

# Creating columns
q1 = result
q1["playstyle"] = np.where(df['air_time'] >= mean_air_time, "air", "ground")

print("Ground, Air (Total)")
print(q1.query("playstyle == 'ground' and winner and event_split == 'Fall'").shape[0],
     q1.query("playstyle == 'air' and winner and event_split == 'Fall'").shape[0])
print(q1.query("playstyle == 'ground' and winner and event_split == 'Winter'").shape[0],
     q1.query("playstyle == 'air' and winner and event_split == 'Winter'").shape[0])
print(q1.query("playstyle == 'ground' and winner and event_split == 'Spring'").shape[0],
     q1.query("playstyle == 'air' and winner and event_split == 'Spring' ").shape[0])
print(q1.query("playstyle == 'ground' and winner and event_split == 'Summer'").shape[0],
     q1.query("playstyle == 'air' and winner and event_split == 'Summer'").shape[0])

print("Ground, Air (Majors)")
print(q1.query("playstyle == 'ground' and winner and event_split == 'Fall' and event == 'Major'").shape[0],
     q1.query("playstyle == 'air' and winner and event_split == 'Fall' and event == 'Major'").shape[0])
print(q1.query("playstyle == 'ground' and winner and event_split == 'Winter' and event == 'Major'").shape[0],
     q1.query("playstyle == 'air' and winner and event_split == 'Winter' and event == 'Major'").shape[0])
print(q1.query("playstyle == 'ground' and winner and event_split == 'Spring' and event == 'Major'").shape[0],
     q1.query("playstyle == 'air' and winner and event_split == 'Spring' and event == 'Major'").shape[0])
print(q1.query("playstyle == 'ground' and winner and event_split == 'Summer'and event == 'World Championship'").shape[0],
     q1.query("playstyle == 'air' and winner and event_split == 'Summer'and event == 'World Championship'").shape[0])

# QUESTION 2: Do players from specific regions play more aggressively or passively than those from other regions 
# (movement_total_distance, core_shot & demos)?
# ANSWER: Yes. NA and EU played significantly more aggressively than the other regions by moving around more, shoooting at the net and demoing.

# Creating columns
q2 = result
q2["agg_pass"] = np.where((df['movement_total_distance'] >= mean_air_time) & 
                                    (df['core_shots'] >= mean_shots) & 
                                    (df['demo_inflicted'] >= mean_demos), "aggressive", "passive")

agg_count = {
    "Oceania": 0,
    "North America": 0,
    "South America": 0,
    "Europe": 0,
    "Middle East & North Africa": 0,
    "Sub-Saharan Africa": 0,
    "Asia-Pacific North": 0,
    "Asia-Pacific South": 0
}

agg_count["Oceania"] = q2.query("agg_pass == 'aggressive' and winner and team_region == 'Oceania'").shape[0]
agg_count["North America"] = q2.query("agg_pass == 'aggressive' and winner and team_region == 'North America'").shape[0]
agg_count["South America"] = q2.query("agg_pass == 'aggressive' and winner and team_region == 'South America'").shape[0]
agg_count["Europe"] = q2.query("agg_pass == 'aggressive' and winner and team_region == 'Europe'").shape[0]
agg_count["Middle East & North Africa"] = q2.query("agg_pass == 'aggressive' and winner and team_region == 'Middle East & North Africa'").shape[0]
agg_count["Sub-Saharan Africa"] = q2.query("agg_pass == 'aggressive' and winner and team_region == 'Sub-Saharan Africa'").shape[0]
agg_count["Asia-Pacific North"] = q2.query("agg_pass == 'aggressive' and winner and team_region == 'Asia-Pacific North'").shape[0]
agg_count["Asia-Pacific South"] = q2.query("agg_pass == 'aggressive' and winner and team_region == 'Asia-Pacific South'").shape[0]

print(agg_count)

#print("Aggressive, Passive (Total)")
#print(q2.query("agg_pass == 'aggressive' and winner and event_split == 'Winter'").shape[0],
#     q2.query("agg_pass == 'passive' and winner and event_split == 'Winter'").shape[0])
#print(q2.query("agg_pass == 'aggressive' and winner and event_split == 'Spring'").shape[0],
#     q2.query("agg_pass == 'passive' and winner and event_split == 'Spring' ").shape[0])
#print(q2.query("agg_pass == 'aggressive' and winner and event_split == 'Summer'").shape[0],
#     q2.query("agg_pass == 'passive' and winner and event_split == 'Summer'").shape[0])

#print("Aggressive, Passive (Majors)")
#print(q2.query("agg_pass == 'aggressive' and winner and event_split == 'Fall' and event == 'Major'").shape[0],
#     q2.query("agg_pass == 'passive' and winner and event_split == 'Fall' and event == 'Major'").shape[0])
#print(q2.query("agg_pass == 'aggressive' and winner and event_split == 'Winter' and event == 'Major'").shape[0],
#     q2.query("agg_pass == 'passive' and winner and event_split == 'Winter' and event == 'Major'").shape[0])
#print(q2.query("agg_pass == 'aggressive' and winner and event_split == 'Spring' and event == 'Major'").shape[0],
#     q2.query("agg_pass == 'passive' and winner and event_split == 'Spring' and event == 'Major'").shape[0])
#print(q2.query("agg_pass == 'aggressive' and winner and event_split == 'Summer'and event == 'World Championship'").shape[0],
#     q2.query("agg_pass == 'passive' and winner and event_split == 'Summer'and event == 'World Championship'").shape[0])
#print("//////////////////////////////")

#/////////////////////////////////////////////

# QUESTION 3: What percentage of 'interesting' games were there? (Interesting here is games with a higher than avg save count)
# ANSWER: Signifcant increase in interseting games across the season. Rapid spike in world championships

q3 = result
q3["interesting"] = np.where(df['core_saves'] > mean_save_count, True, False)
print(q3.query("interesting and event_split == 'Winter'").shape[0]/q3.query("event_split == 'Winter'").shape[0])
print(q3.query("interesting and event_split == 'Fall'").shape[0]/q3.query("event_split == 'Fall'").shape[0])
print(q3.query("interesting and event_split == 'Spring'").shape[0]/q3.query("event_split == 'Spring'").shape[0])
print(q3.query("interesting and event_split == 'Summer'").shape[0]/q3.query("event_split == 'Summer'").shape[0])

# QUESTION 4: Which teams (and which regions) have more teamwork involved (looking at team assists here, not wins)
# ANSWER: G2 Esports. One of the most famous e-sports organizations

q4 = result
q4["teamwork"] = np.where(df['core_assists'] > mean_assists, True, False)
q4_2 = q4.loc[q4['teamwork']]
top_teamwork_teams = q4_2['team_name'].value_counts().head()#.idxmax()
top_teamwork_teams