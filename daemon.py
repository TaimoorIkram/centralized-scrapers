"""
The daemon is supposed to be the listener to which
system commands are sent to start the scrapers. But
this class is not currently working properly.
"""

import os

def start_scraper(scraper_path):
    os.system('python ./scripts/daraz.py')


start_scraper('skibidi.py')