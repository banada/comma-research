import numpy as np
import h5py
from tools.lib.logreader import LogReader

# Run this from 'openpilot/tools/lib'

# TODO take argument
log = LogReader("2021-09-29--13-46-36")
project_dir="/home/banada/comma-research"
name="test-crop-center"

# The frame rate is lower than the sample rate, so we downsample
frame = 0
wheel_speeds = []
steer_angles = []
frames = []

for msg in log:
  if msg.which() == "cameraOdometry":
    frame += 1
    frames.append(frame)
  if msg.which() == "carState":
    if (len(wheel_speeds) < frame):
      wheel_speeds.append(msg.carState.wheelSpeeds)
  if msg.which() == "carControl":
    if (len(steer_angles) < frame):
      steer_angles.append(msg.carControl.actuatorsOutput.steeringAngleDeg)

print(f"{frame} frames")
wheel_speeds = np.array(wheel_speeds)
steer_angles = np.array(steer_angles)
frames = np.array(frames)
print(f"wheel speeds: {wheel_speeds.shape}")
print(f"steering angles: {steer_angles.shape}")

with h5py.File(f"{project_dir}/dataset/log/{name}.h5", "w") as file:
  steering_angle = file.create_dataset("steering_angle", steer_angles.shape, data=steer_angles)
  frame_count = file.create_dataset("frame", frames.shape, data=frames)
  print(steering_angle)
