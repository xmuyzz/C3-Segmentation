# C3-Segmentation

The codebase for auto-segmenting the C3 skeletal muscle mass, muscle cross-sectional area (CSA), and Skeletal Mass Index (SMI) from 3D CT images.

Consists of two deep-learning models: Slice Selection Model and Segmentation Model. The Slice Selection Model is adapted from DenseNet and the Segmentation model is adapted from UNet.


### Trained Model Weights 

Model Weights are available for download at the following link.

https://drive.google.com/drive/folders/1A3NlgyvlhXL6pgR0weXT4c-XygGl6r-M?usp=drive_link

### Steps before you execute the Scripts listed 

1. Download the model weights from the google drive link provided above, unzip the files, and save them in the 'model' subfolder. Please note that the CV folder within the zip file contains five-fold cross-validation sub-models for segmentation.

2. Make sure the input files are stored in the following folder

   Raw scans - /data/raw_img/

   Suggested directories for storing the data processed in the scripts:
   Pre-processed Scans - /data/prepro_img
   Slice Selection Output CSV - /data/test/output_scv
   Segmentation Model Output - /data/test/output_segmentation 
  
3. Before executing each script, edit the script to point to the correct input/output directories.
   

### Scripts Execution Sequence

1. 'src/Preprocess_test_data.py'

      Set the proj_dir, img_dir, and seg_dir folder paths in the main function before executing the code.
      This script preprocesses the raw scans. The steps involve respacing the input files to 1x1, cropping by 256x256, and resizing to 512x512 along the XY plane.
      - Input: Data folder raw CT scans under the folder of '../data/raw_img'
      - Out_put: Preprocessed files in the folder '..data/prepro_img'
    
3. 'Test_slice_model.py'

4. 'Test_segmentation_model.py'

5. 'get_dice.py'

6. 'statistics.py'

7. 'visualize.py'

8. 'clinical.py'

1. `main.py`  
     Step 1: Execute Slice Selection Model first to select the C3 slice from the raw CT scan file provided as input. (No pre-processing of the raw scans are needed for this step) 
     - Input_1: Data folder raw CT scans under the folder of '../data/'
     - Input_2: a model folder containing the model weights '../model/'
     - Out_put: output_scv.csv containing predicted C3 slice number for each of the CT scans in the input folder.
     - [Further details](..d)

     Step 2: Executes Segmentation Model to produce predicted mask file from selected C3 slide. (Data needs to be pre-processed. The preprocessing steps consist of scaling to pixel width 1, cropping the image with 256x256x1, and then resizing) 
     - Input_1: Data folder raw CT scans under the folder of '../data/'
     - Input_2: a model folder containing the model weights '../model/'
     - Out_put: Segmentation masks in the output folder '../data/test/output_segmentation
     - [Further details](..d)

2. `main.py`  
 
