import fastf1 
import pandas as pd 
import matplotlib.pyplot as plt 

fastf1.Cache.enable_cache('./f1_cache')
session = fastf1.get_session(2021, 'France', 'R')
session.load()

laps = session.laps

pit_stops = []

for drv in laps['Driver'].unique():
    drv_laps = laps.pick_drivers(drv).reset_index(drop=True)

    in_laps = drv_laps[drv_laps['PitInTime'].notna()]

    for _, in_lap in in_laps.iterrows():
        lap_num = in_lap['LapNumber']

        out_lap = drv_laps[drv_laps['LapNumber'] == lap_num + 1]

        if len(out_lap) == 1 and pd.notna(out_lap.iloc[0]['PitOutTime']):
            duration = (out_lap.iloc[0]['PitOutTime'] - in_lap['PitInTime']).total_seconds()
            pit_stops.append({
                'Driver': drv,
                'Team': in_lap['Team'],
                'Lap': lap_num,
                'Duration': duration
            })

pit_df = pd.DataFrame(pit_stops)
print(pit_df.sort_values('Duration').to_string())

team_avg = pit_df.groupby('Team')['Duration'].mean().sort_values()
print("\nAverage pit stop duration by team (seconds):")
print(team_avg)

plt.figure(figsize=(10, 6))
team_avg.plot(kind='barh', color='steelblue')
plt.xlabel('Average Pit Stop Duration (seconds)')
plt.title('2021 French GP — Average Pit Stop Duration by Team')
plt.tight_layout()
plt.savefig('team_pit_durations.png')
plt.show()
