# Author: Joseph Cheatham
# Description: Downloads NEXRAD Level-II data for the 2011 Joplin tornado

import boto3
import os
from botocore import UNSIGNED
from botocore.config import Config

SAVE_DIR = 'nexrad_data'
os.makedirs(SAVE_DIR, exist_ok=True)

BUCKET = 'unidata-nexrad-level2'

s3 = boto3.client(
    's3',
    region_name='us-east-1',
    config=Config(signature_version=UNSIGNED)
)

# Joplin tornado was on the ground ~2234-2312 UTC
# Grabbing 2200-2330 UTC to capture full lifecycle
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