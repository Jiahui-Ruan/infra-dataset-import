#!/usr/bin/env bash

cd $WHERE_THE_BAG_STORE
# inspect the import parameters
ds-rosbag-scan ./out    # looks ok?
# I don't trust my network
tmux
# do real import
ds-rosbag-scan ./out | xargs -L1 -P4 ds-import | tee import-log.log # better to keep log
###### wait for a moment ######

cd out
# optional, compress the video
ls | xargs -L1 ds-compress-video
# ds-check to ensure the sanity
ls | xargs -L1 ds-check # looks good?
# copy to /truenas/datasets
cp -r * ~/datasets_writable # a writable mount point of /truenas/datasets
# submit to server
ls | xargs -L1 ds-submit # should return all trues
