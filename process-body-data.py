import os
import sys
import numpy as np
import h5py
import skvideo.io
from tools.lib.logreader import LogReader

# Run this from 'openpilot/tools/lib'

path = sys.argv[1]
log = f"{path}/rlog"
cam = f"{path}/dcamera-crop-center.hevc"
segment_path = os.path.dirname(path)
segment = os.path.basename(segment_path)
project_dir = "{HOME}/comma-research".format(**os.environ)

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

with h5py.File(f"{project_dir}/dataset/log/{segment}.h5", "w") as logfile:
  steering_angle_ds = logfile.create_dataset("steering_angle", steer_angles.shape, data=steer_angles)
  speed_ds = logfile.create_dataset("speed", speed.shape, data=speed)
  frame_ds = logfile.create_dataset("frame", frames.shape, data=frames)

# HEVC to HDF5
print(f"Processing {cam}")
video = skvideo.io.vread(cam)
with h5py.File(f"{project_dir}/dataset/camera/{segment}.h5", "w") as camfile:
  x = camfile.create_dataset("X", video.shape, data=video)

print(f"Done processing")

