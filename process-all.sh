#!/bin/bash

FILES=("dcamera-crop-center.hevc" "dcamera-shift-left.hevc" "dcamera-shift-right.hevc" "dcamera-shift-up.hevc" "dcamera-shift-down.hevc")

for DIR in $BODY_VIDEO_DIR/*; do
  for FILE in ${FILES[@]}; do
    python process-body-data.py $DIR/ $FILE
  done
done
