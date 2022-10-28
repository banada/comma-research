# comma body steering angle predictor

Based on [comma.ai's research](https://github.com/commaai/research), adapted for the comma body.

## Credits

Riccardo Biasini, George Hotz, Sam Khalandovsky, Eder Santana, and Niel van der Westhuizen

## Requirements
[anaconda](https://www.continuum.io/downloads)  
[tensorflow-0.9](https://github.com/tensorflow/tensorflow)  
[keras-1.0.6](https://github.com/fchollet/keras)  
[cv2](https://anaconda.org/menpo/opencv3)

## Pipeline

`sort-videos.sh` is an interactive script to preview and sort videos from the body.

`augment-videos.sh` is used to turn one video into many through viewport manipulation (cropping and translating).

`video2hdf5.py` converts HEVC and rlog to HDF5. These depend on openpilot and should be run from `openpilot/tools/lib`.
TODO: separate out openpilot dependency

`split-dataset.py` splits the training and validation sets
TODO: split test set as well

Run the servers in separate terminals and train:
```
./server.py --batch 200 --port 5557
./server.py --batch 200 --validation --port 5556
./train_steering_model.py --port 5557 --val_port 5556 --epoch X
./view_steering_model.py ./outputs/steering_model/steering_angle.json --dataset={TEST_FILE_NAME}
```

## Setup

### Environment variables:
`$BODY_VIDEO_DIR` should contain all HEVC video files
`$BODY_DATASET_DIR` should contain:
```
camera/
log/
```

The dataset folder structure is the following:
```bash
+-- dataset
|   +-- camera
|   |   +-- 2016-04-21--14-48-08
|   |   ...
|   +-- log
|   |   +-- 2016-04-21--14-48-08
|   |   ...
```

All the files come in hdf5 format and are named with the time they were recorded.
The camera dataset has shape `number_frames x 3 x 160 x 320` and `uint8` type.
between camera frames and the other measurements.

