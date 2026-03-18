# Author: Joseph Cheatham
# Description: Verify rotation signature location against known Joplin coordinates

import pyart
import matplotlib.pyplot as plt
import numpy as np
import os

SAVE_DIR = 'nexrad_data'
PLOT_DIR = 'plots'

SCAN = os.path.join(SAVE_DIR, 'KSGF20110522_224838_V03.gz')
radar = pyart.io.read(SCAN)

# KSGF radar location
radar_lat = float(radar.latitude['data'][0])
radar_lon = float(radar.longitude['data'][0])
print(f'Radar location: {radar_lat:.4f}N, {radar_lon:.4f}W')

# Convert Joplin city center lat/lon to radar-relative x/y km
# Simple approximation: 1 degree lat ~ 111 km, 1 degree lon ~ 111*cos(lat) km
joplin_lat = 37.08
joplin_lon = -94.51

dx = (joplin_lon - radar_lon) * 111.0 * np.cos(np.radians(radar_lat))
dy = (joplin_lat - radar_lat) * 111.0

print(f'Joplin city center in radar coords: x={dx:.1f} km, y={dy:.1f} km')

# Plot zoomed velocity with Joplin marker overlaid
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('Zoomed - Joplin Area - 2248 UTC (with ground truth)', fontsize=13)

display = pyart.graph.RadarDisplay(radar)

display.plot_ppi('reflectivity', sweep=0, ax=axes[0],
                 vmin=0, vmax=75, title='Reflectivity',
                 colorbar_label='dBZ')
display.set_limits(xlim=(-145, -70), ylim=(-80, -10), ax=axes[0])
axes[0].plot(dx, dy, 'w*', markersize=15, label='Joplin center')
axes[0].legend(loc='lower right')

display.plot_ppi('velocity', sweep=1, ax=axes[1],
                 vmin=-30, vmax=30, title='Velocity',
                 colorbar_label='m/s', cmap='RdBu_r')
display.set_limits(xlim=(-145, -70), ylim=(-80, -10), ax=axes[1])
axes[1].plot(dx, dy, 'w*', markersize=15, label='Joplin center')
axes[1].legend(loc='lower right')

plt.tight_layout()
outpath = os.path.join(PLOT_DIR, 'step3_ground_truth.png')
plt.savefig(outpath, dpi=150, bbox_inches='tight')
print(f'Saved {outpath}')
plt.show()