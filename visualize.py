# Author: Joseph Cheatham
# Description: Visualize reflectivity and velocity on correct sweeps

import pyart
import matplotlib.pyplot as plt
import os

SAVE_DIR = 'nexrad_data'
PLOT_DIR = 'plots'
os.makedirs(PLOT_DIR, exist_ok=True)

SCAN = os.path.join(SAVE_DIR, 'KSGF20110522_224838_V03.gz')

print(f'Reading {os.path.basename(SCAN)}...')
radar = pyart.io.read(SCAN)

display = pyart.graph.RadarDisplay(radar)

# Plot 1: Full view

fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('KSGF - Joplin Tornado - 2248 UTC May 22 2011', fontsize=13)

display.plot_ppi('reflectivity', sweep=0, ax=axes[0],
                 vmin=0, vmax=75, title='Reflectivity (sweep 0, 0.48°)',
                 colorbar_label='dBZ')
display.set_limits(xlim=(-150, 150), ylim=(-150, 150), ax=axes[0])

display.plot_ppi('velocity', sweep=1, ax=axes[1],
                 vmin=-30, vmax=30, title='Velocity (sweep 1, 0.48°)',
                 colorbar_label='m/s', cmap='RdBu_r')
display.set_limits(xlim=(-150, 150), ylim=(-150, 150), ax=axes[1])

plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, 'step1_ref_vel.png'), dpi=150, bbox_inches='tight')
print('Saved step1_ref_vel.png')

# Plot 2: Zoomed into Joplin area
# Joplin is SW of KSGF — approximately -100km x, -50km y
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('Zoomed - Joplin Area - 2248 UTC', fontsize=13)

display2 = pyart.graph.RadarDisplay(radar)

display2.plot_ppi('reflectivity', sweep=0, ax=axes[0],
                  vmin=0, vmax=75, title='Reflectivity (Zoomed)',
                  colorbar_label='dBZ')
display2.set_limits(xlim=(-130, -70), ylim=(-80, -20), ax=axes[0])

display2.plot_ppi('velocity', sweep=1, ax=axes[1],
                  vmin=-30, vmax=30, title='Velocity (Zoomed)',
                  colorbar_label='m/s', cmap='RdBu_r')
display2.set_limits(xlim=(-130, -70), ylim=(-80, -20), ax=axes[1])

plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, 'step2_zoomed.png'), dpi=150, bbox_inches='tight')
print('Saved step2_zoomed.png')
