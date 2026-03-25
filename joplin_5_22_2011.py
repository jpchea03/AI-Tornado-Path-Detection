# Title: joplin_5_22_2011.py
# Author: Joseph Cheatham
# Description: Downloads and visualizes NEXRAD Level-II data for the 2011 Joplin tornado

import boto3
import os
from botocore import UNSIGNED
from botocore.config import Config
import pyart
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

SAVE_DIR = 'nexrad_data'
os.makedirs(SAVE_DIR, exist_ok=True)

BUCKET = 'unidata-nexrad-level2'

s3 = boto3.client(
    's3',
    region_name='us-east-1',
    config=Config(signature_version=UNSIGNED)
)

# Radar scan files from s3
TORNADO_SCANS = [
    '2011/05/22/KSGF/KSGF20110522_220959_V03.gz',
    '2011/05/22/KSGF/KSGF20110522_221449_V03.gz',
    '2011/05/22/KSGF/KSGF20110522_221938_V03.gz',
    '2011/05/22/KSGF/KSGF20110522_222428_V03.gz',
    '2011/05/22/KSGF/KSGF20110522_222919_V03.gz',
    '2011/05/22/KSGF/KSGF20110522_223408_V03.gz',
    '2011/05/22/KSGF/KSGF20110522_223858_V03.gz',
    '2011/05/22/KSGF/KSGF20110522_224348_V03.gz',
    '2011/05/22/KSGF/KSGF20110522_224838_V03.gz',
    '2011/05/22/KSGF/KSGF20110522_225328_V03.gz',
    '2011/05/22/KSGF/KSGF20110522_225818_V03.gz',
    '2011/05/22/KSGF/KSGF20110522_230307_V03.gz',
    '2011/05/22/KSGF/KSGF20110522_230757_V03.gz',
    '2011/05/22/KSGF/KSGF20110522_231247_V03.gz',
    '2011/05/22/KSGF/KSGF20110522_231736_V03.gz',
    '2011/05/22/KSGF/KSGF20110522_232226_V03.gz',
    '2011/05/22/KSGF/KSGF20110522_232716_V03.gz',
]

def download_scan(key):
    filename = os.path.basename(key)
    save_path = os.path.join(SAVE_DIR, filename)

    if os.path.exists(save_path):
        print(f'  Already have {filename}, skipping.')
        return save_path

    try:
        print(f'  Downloading {filename}...')
        s3.download_file(BUCKET, key, save_path)
        print(f'  Saved.')
        return save_path
    except Exception as e:
        print(f'  Failed: {e}')
        return None
    
print(f'Downloading {len(TORNADO_SCANS)} scans...\n')
downloaded = []
for key in TORNADO_SCANS:
    path = download_scan(key)
    if path:
        downloaded.append(path)

print(f'\nDone. {len(downloaded)}/{len(TORNADO_SCANS)} files saved to {SAVE_DIR}/')
print('\nFiles:')
for f in sorted(os.listdir(SAVE_DIR)):
    print(f'  {f}')

print('All done!')

# --5:34PM CDT--
scan_path = downloaded[5]
print(f'\nVisualizing {os.path.basename(scan_path)}...')
radar = pyart.io.read_nexrad_archive(scan_path)

fig = plt.figure(figsize=(16, 8))

# Reflectivity
ax1 = fig.add_subplot(1, 2, 1, projection=ccrs.PlateCarree())
display = pyart.graph.RadarMapDisplay(radar)
display.plot_ppi_map(
    'reflectivity',
    sweep=0,
    ax=ax1,
    vmin=-20, vmax=75,
    min_lon=-95.5, max_lon=-93.5,
    min_lat=36.5, max_lat=38.0,
    resolution='10m',
    cmap='NWSRef',
)
ax1.set_title('Reflectivity – 22:34 UTC')

# Velocity
ax2 = fig.add_subplot(1, 2, 2, projection=ccrs.PlateCarree())
display2 = pyart.graph.RadarMapDisplay(radar)
display2.plot_ppi_map(
    'velocity',
    sweep=1,
    ax=ax2,
    vmin=-30, vmax=30,
    min_lon=-95.5, max_lon=-93.5,
    min_lat=36.5, max_lat=38.0,
    resolution='10m',
    cmap='NWSVel',
)
ax2.set_title('Velocity – 22:34 UTC')

plt.suptitle('KSGF – 22:34 UTC (5:34 PM CDT) May 22, 2011', fontsize=14)
plt.tight_layout()
plt.savefig('plots/joplin_ref_vel_2234.png', dpi=150)
plt.show()


# 5:39 PM CDT
scan_path = downloaded[6]
print(f'\nVisualizing {os.path.basename(scan_path)}...')
radar = pyart.io.read_nexrad_archive(scan_path)
fig = plt.figure(figsize=(16, 8))

# Reflectivity
ax1 = fig.add_subplot(1, 2, 1, projection=ccrs.PlateCarree())
display = pyart.graph.RadarMapDisplay(radar)
display.plot_ppi_map(
    'reflectivity',
    sweep=0,
    ax=ax1,
    vmin=-20, vmax=75,
    min_lon=-95.5, max_lon=-93.5,
    min_lat=36.5, max_lat=38.0,
    resolution='10m',
    cmap='NWSRef',
)
ax1.set_title('Reflectivity – 22:39 UTC')

# Velocity
ax2 = fig.add_subplot(1, 2, 2, projection=ccrs.PlateCarree())
display2 = pyart.graph.RadarMapDisplay(radar)
display2.plot_ppi_map(
    'velocity',
    sweep=1,
    ax=ax2,
    vmin=-30, vmax=30,
    min_lon=-95.5, max_lon=-93.5,
    min_lat=36.5, max_lat=38.0,
    resolution='10m',
    cmap='NWSVel',
)
ax2.set_title('Velocity – 22:39 UTC')

plt.suptitle('KSGF – 22:39 UTC (5:39 PM CDT) May 22, 2011', fontsize=14)
plt.tight_layout()
plt.savefig('plots/joplin_ref_vel_2239.png', dpi=150)
plt.show()