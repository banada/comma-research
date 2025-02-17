import os
import sys
import numpy as np
import h5py
import skvideo.io
from tools.lib.logreader import LogReader

# Run this from 'openpilot/tools/lib'

files = [
  "dcamera-crop-center.hevc",
  "dcamera-shift-left.hevc",
  "dcamera-shift-right.hevc",
  "dcamera-shift-up.hevc",
  "dcamera-shift-down.hevc"
]

def create_hdf5(path, file):
  # Augmented data filenames
  shift = file.replace('.hevc', '')
  shift = shift.replace('dcamera-', '')
  log = f"{path}/rlog"
  cam = f"{path}/{file}"
  segment = os.path.basename(path)
  dataset_dir = os.environ.get('BODY_DATASET_DIR')

  # The frame rate is lower than the sample rate, so we downsample
  frame = 0
  frames = []
  speed = []
  steer_angles = []

  # rlog to HDF5
  print(f"Processing {log}")
  logreader = LogReader(log)
  for msg in logreader:
    if msg.which() == "cameraOdometry":
      frame += 1
      frames.append(frame)
    if msg.which() == "carState":
      if (len(speed) < frame):
        speed.append(msg.carState.vEgo)
    if msg.which() == "carControl":
      if (len(steer_angles) < frame):
        steer_angles.append(msg.carControl.actuatorsOutput.steeringAngleDeg)

  print(f"Processed {frame} log frames")
  speed = np.array(speed)
  steer_angles = np.array(steer_angles)
  frames = np.array(frames)

  with h5py.File(f"{dataset_dir}/log/{segment}-{shift}.h5", "w") as logfile:
    steering_angle_ds = logfile.create_dataset("steering_angle", steer_angles.shape, data=steer_angles)
    speed_ds = logfile.create_dataset("speed", speed.shape, data=speed)
    frame_ds = logfile.create_dataset("frame", frames.shape, data=frames)

  # HEVC to HDF5
  print(f"Processing {cam}")
  video = skvideo.io.vread(cam)
  with h5py.File(f"{dataset_dir}/camera/{segment}-{shift}.h5", "w") as camfile:
    x = camfile.create_dataset("X", video.shape, data=video)

  print(f"Done processing")


body_video_dir = os.environ.get('BODY_VIDEO_DIR')
for directory in os.listdir(body_video_dir):
  for filename in files:
    create_hdf5(f'{body_video_dir}/{directory}', filename)


