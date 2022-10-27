#!/bin/bash

# sort-videos.sh
#
# Plays each HEVC video in a directory
# Users kills VLC, then answers the prompt
# Moves directories into keep/junk dirs

KEEP_DIR="./keepers"
JUNK_DIR="./junk"

mkdir -p $KEEP_DIR
mkdir -p $JUNK_DIR
echo ""

function prompt_to_keep() {
  echo ""
  echo "Include this video? y / n / Next (Enter)"
  read KEEP
}

for DIR in $PWD/*; do
  if [ ! -d $DIR ]; then
    continue
  fi
  echo "Checking $DIR"

  for FILE in $DIR/*.hevc; do
    if [ ! -e $FILE ]; then
      echo "End of directory."
      prompt_to_keep
      if [ "$KEEP" = "y" ]; then
        mv $DIR $KEEP_DIR
        break
      else
        mv $DIR $JUNK_DIR
        break
      fi
      continue
    fi
    echo "Playing $FILE"
    vlc $FILE > /dev/null 2>&1
    prompt_to_keep
    if [ "$KEEP" = "y" ]; then
      mv $DIR $KEEP_DIR
      break
    elif [ "$KEEP" = "n" ]; then
      mv $DIR $JUNK_DIR
      break
    else
      echo "Next video"
      continue
    fi
  done
done
