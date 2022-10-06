#!/usr/bin/env python

import h5py
import numpy as np
import skvideo.io

path = "test-crop-center.hevc"
# TODO with/as?
video = skvideo.io.vread(path)

# Cast to list to re-arrange shape
# TODO rearrange video?
# TODO or just rewrite concatenate function
#sl = slice(3)
#x_shape = list(video.shape[sl])
#x_shape.insert(1, video.shape[3])
#x_shape = tuple(x_shape)

with h5py.File("./dataset/camera/test-crop-center.h5", "w") as file:
  x = file.create_dataset("X", video.shape, data=video)
  print(x)

