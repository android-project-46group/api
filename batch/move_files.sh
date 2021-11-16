#!/bin/sh
#
# Description:
#   Move(copy) images to /var/www/ folder
#

# Copy images to /var/www/html/imgs.
IMG_DIR='/home/ubuntu/work/python/api/batch/imgs'
WWW_IMG_DIR='/var/www/html/imgs/blog'
sudo cp -r "${IMG_DIR}/hinata/" "${WWW_IMG_DIR}/"
sudo cp -r "${IMG_DIR}/sakura/" "${WWW_IMG_DIR}/"
sudo cp -r "${IMG_DIR}/nogi/" "${WWW_IMG_DIR}/"

# Copy json files to folder of golang.
BLOG_INFO_DIR='/home/ubuntu/work/python/api/batch/outputs'
BLOG_INFO_GO_DIR='/home/ubuntu/work/go/web/db/data/blogs'
ls "${BLOG_INFO_DIR}/" | xargs -I@ cp -f "${BLOG_INFO_DIR}/"@ "${BLOG_INFO_GO_DIR}/"
