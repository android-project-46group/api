#!/bin/sh
#
# Description:
#   Three steps to update blogs db.
#   1. Scraping images and updated time.
#   2. Move images and jsons to appropriate places.
#   3. Update postgresql using golang batch.
#
# Usage:
#   bash night_batch.sh
# (0 0 * * * bash /home/ubuntu/work/python/api/night_batch.sh)

PYTHON_DIR="/home/ubuntu/work/python/api/batch"
GO_DIR="/home/ubuntu/work/go/web"

# step 1
bash ${PYTHON_DIR}/update_blog_json.sh
# step 2
bash ${PYTHON_DIR}/move_files.sh
# step 3
${GO_DIR}/night_batch
