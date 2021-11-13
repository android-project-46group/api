#!/bin/sh

python hinatazaka_blog_latest.py
python nogizaka_blog_latest.py
python sakura_blog_latest.py

python make_outputs.py
