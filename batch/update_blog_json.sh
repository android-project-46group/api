#!/bin/sh
#
# Description:
#   Scraping Part.
#   Download images and make json.
#

DIR='/home/ubuntu/work/python/api/batch'

# scraping
python3 ${DIR}/hinatazaka_blog_latest.py
python3 ${DIR}/nogizaka_blog_latest.py
python3 ${DIR}/sakura_blog_latest.py

# make json file
python3 ${DIR}/make_outputs.py
