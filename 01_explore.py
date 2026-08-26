import fastf1 

fastf1.Cache.enable_cache('./f1_cache')

session = fastf1.get_session(2021, 'France', 'R') 
session.load()

print(session.event['EventName'], session.event['EventDate'])
print(len(session.laps), "laps loaded")
print("Drivers:", sorted(session.laps['Driver'].unique()))
