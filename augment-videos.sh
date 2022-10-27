#!/bin/bash

echo ""
echo "=================================="
echo "=   comma body video augmenter   ="
echo "=================================="
echo ""

function help {
  echo "Usage: ./augment-videos.sh <options>"
  echo "  -c, --center:        Crop center"
  echo "  -w, --width <int>:   Video output width"
  echo "  -h, --height <int>:  Video output height"
  echo ""
  #  echo "  -m, --mp4:           Convert to mp4"
  #ffmpeg -y -r 20 -i $FILE -c copy -map 0 -vtag hvc1 $NAME.mp4
  exit 1
}

CROP_CENTER=0
WIDTH=320
HEIGHT=160
FILES=("dcamera.hevc" "ecamera.hevc" "fcamera.hevc")

if [[ $# -lt 1 ]]; then
  help
fi

while [[ $# -gt 0 ]]; do
  KEY=$1
  VAL=$2
  case "$KEY" in
    -c|--center)
      CROP_CENTER=1
      shift
      ;;
    -w|--width)
      WIDTH=$VAL
      shift
      shift
      ;;
    -e|--height)
      HEIGHT=$VAL
      shift
      shift
      ;;
    -h|--help)
      help
      shift
      ;;
  esac
done

for DIR in $PWD/*; do
  if [ ! -d $DIR ]; then
    continue
  fi
  echo "checking $DIR"

  for FILE in ${FILES[@]}; do
    FILE=$DIR/$FILE
    if [ ! -e $FILE ]; then
      continue
    fi
    if [ $CROP_CENTER -gt 0 ]; then
      echo "  cropping $WIDTH x $HEIGHT in the center of $FILE"
      NAME=$(echo "$FILE" | sed "s/\.hevc//;")
      CROP_NAME=$NAME-crop-center.hevc
      if [ -e $CROP_NAME ]; then
        echo "$CROP_NAME exists, skipping"
        continue
      fi
      ffmpeg -y -i $FILE -filter:v "crop=$WIDTH:$HEIGHT" $CROP_NAME
      echo "  saved $CROP_NAME"
    fi
  done
  echo ""
done

exit 0
