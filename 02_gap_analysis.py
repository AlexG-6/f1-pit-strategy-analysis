import fastf1 
import matplotlib.pyplot as plt

fastf1.Cache.enable_cache('./f1_cache')
session = fastf1.get_session(2021, 'France', 'R') 
session.load()

laps = session.laps

ver = laps.pick_drivers('VER')[['LapNumber', 'Time', 'PitInTime']].reset_index(drop=True)
ham = laps.pick_drivers('HAM')[['LapNumber', 'Time', 'PitInTime']].reset_index(drop=True)

merged = ver.merge(ham, on='LapNumber', suffixes=('_VER', '_HAM'))

merged['gap_seconds'] = (merged['Time_HAM'] - merged['Time_VER']).dt.total_seconds()

print(merged[['LapNumber', 'gap_seconds']].to_string())


ver_pit_laps = merged.loc[merged['PitInTime_VER'].notna(), 'LapNumber'].tolist()
ham_pit_laps = merged.loc[merged['PitInTime_HAM'].notna(), 'LapNumber'].tolist()
print("VER pitted on lap(s):", ver_pit_laps)
print("HAM pitted on lap(s):", ham_pit_laps)

plt.figure(figsize=(11, 6.5))

plt.fill_between(merged['LapNumber'], merged['gap_seconds'], 0,
                  where=(merged['gap_seconds'] < 0), color='#1E5BC6', alpha=0.15, label='Hamilton ahead')
plt.fill_between(merged['LapNumber'], merged['gap_seconds'], 0,
                  where=(merged['gap_seconds'] >= 0), color='#C6291E', alpha=0.15, label='Verstappen ahead')

plt.plot(merged['LapNumber'], merged['gap_seconds'], color='black', linewidth=1.5)
plt.axhline(0, color='gray', linewidth=0.8)

ymin, ymax = -24, 6  
plt.ylim(ymin, ymax)


for lap in ver_pit_laps:
    plt.axvline(lap, color='#C6291E', linestyle='--', alpha=0.6)
plt.text(ver_pit_laps[0] - 0.3, ymin + 1, 'VER pit', color='#C6291E', fontsize=9, ha='right')
plt.text(ver_pit_laps[1] - 0.3, ymin + 1, 'VER pit', color='#C6291E', fontsize=9, ha='right')

for lap in ham_pit_laps:
    plt.axvline(lap, color='#1E5BC6', linestyle='--', alpha=0.6)
plt.text(ham_pit_laps[0] + 0.3, ymin + 1, 'HAM pit', color='#1E5BC6', fontsize=9, ha='left')


plt.title('Verstappen vs Hamilton — Race Gap, 2021 French GP', pad=20)

plt.annotate('Undercut: VER takes\nthe lead after both pit stops',
             xy=(20, 0.65), xytext=(23, 4.5),
             arrowprops=dict(arrowstyle='->', color='gray', 
                              connectionstyle='arc3,rad=0.2'), 
             fontsize=9)

plt.annotate('VER passes HAM on-track\n(lap 52 of 53)',
             xy=(51.5, 0.5), xytext=(35, -19),
             arrowprops=dict(arrowstyle='->', color='gray',
                              connectionstyle='arc3,rad=-0.2'), 
             fontsize=9)

plt.xlabel('Lap Number')
plt.ylabel('Gap (seconds) — positive = Verstappen ahead')
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig('ver_ham_gap.png', dpi=150)
plt.show()