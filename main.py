import subprocess
from utils import *
from pytz import timezone
import datetime
import pathlib
import json

# Check existing pwc files version
if os.path.isfile('./input/papers-with-abstracts.json'):
    fname = pathlib.Path('./input/papers-with-abstracts.json')
    mtime = datetime.datetime.fromtimestamp(fname.stat().st_mtime, tz=timezone('US/Eastern'))
    print("Files from Papers_With_Code are updated at: ", mtime)

# Download pwc files
inp = input("Do you want to update files from Papers_With_Code? [y/n] ")
if inp.lower() == "y":
    print("Ok. We are now downloading from Papers_With_Code...")
    subprocess.call(['sh', './getPwC.sh'])

# Craw dataset names
crawled = os.path.isfile('./input/papers-with-abstracts-datasets.json')
if not crawled:
    # if not crawled before, crawled for all papers
    crawl_dataset_names(old_papers=[])
else:
    # if crawled before, crawled for new papers
    inp = input("Do you want to crawled for new papers from Papers_With_Code? [y/n] ")
    old_papers =  json.load(open('./input/papers-with-abstracts-datasets.json'))
    old_papers = [p['paper_url'] for p in old_papers]
    if inp == 'y':
        crawl_dataset_names(old_papers=old_papers)

