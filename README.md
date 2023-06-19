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
    
2. 'test_slice_model.py'

      Set the proj_dir, raw_img_dir, model_path, and slice_csv_path directories before executing the code. 
      This script tests the slice selection model which predicts C3 slice for each raw_scan given as input. Please note that input files are raw CT scans. 
	   - Input Scans: nrrd files
      - Model: C3_Top_Selection_Model_Weight.hdf5 
 	   - Output: C3_Top_Slice_Prediction.csv' 


3. 'test_segmentation_model.py'

4. 'get_dice.py'

5. 'statistics.py'

6. 'visualize.py'

7. 'clinical.py'

