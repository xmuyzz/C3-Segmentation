# C3-Segmentation

Code base for auto segmenting the skeletal muscle mass from 3D CT images

Consists of two deep-learning models: Slice Selection Model and Segmentation Model

Slice Selection Model is adpated from DenseNet and Segmentation model is adapted from UNet

C3 auto-segmentation for muscle cross section area

### Scripts Execution Sequence

1. `main.py`  
     Step 1: Executes Slice Slection Model first to select the C3 slice from the raw CT scan file provided as input. (No pre-processing of the raw scans are needed for this step) 
     - Input_1: Data folder raw CT scans under the folder of '../data/'
     - Input_2: model folder cantaining the model weights '../model/'
     - Out_put: output_scv.csv containing predicted C3 slice number for each of the CT scans in input folder.
     - [Further details](..d)

     Step 2: Executes Segmenation Model to produced predicted mask file from selectd C3 slide. (Data needs to be pre-processed. The preprocessing steps consist of scaling to pixel width 1, cropping the image with 256x256x1 and then resized) 
     - Input_1: Data folder raw CT scans under the folder of '../data/'
     - Input_2: model folder cantaining the model weights '../model/'
     - Out_put: Segmention masks in the output folder '../data/test/output_segmentation
     - [Further details](..d)

2. `main.py`  
 
