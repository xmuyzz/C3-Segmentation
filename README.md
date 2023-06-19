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

   	Set the proj_dir, raw_img_dir, model_path, slice_csv_path, and output_dir directories before executing the code. 
	This script generates the segmentation masks for the selected C3 slice for each raw_scan given as input.
   	- Input Scans: nrrd files
 	- Model: C3_Top_Segmentation_Model_Weight.hdf5 
 	- Input: C3_Top_Slice_Prediction.csv
 	- Output: Segmentation masks in output_dir


4. 'get_dice.py'

   	Set the proj_dir, raw_img_dir, raw_seg_dir, Slice Prediction CSV, and output_dir directories before executing the code. 
	This script generates the Dice scores for auto-segmentation masks when manual segmentations of test data are available.
   	- Input#1 : Auto segmentation files
 	- Input#2: Manual segmentation files of test data
 	- Input#3: C3_Top_Slice_Prediction.csv
 	- Output: DICE Scores of test data in a CSV file

5. 'get_CSA.py'

  	Set the proj_dir, raw_img_dir, raw_seg_dir, Slice Prediction CSV, and output_dir directories before executing the code. 
	This script generates the Cross-Sectional Area (CSA) of the C3 Skeletal Muscle Mass from the auto-segmented masks.
   	- Input#1 : Auto segmentation files
 	- Input#2: Manual segmentation files of test data
 	- Input#3: C3_Top_Slice_Prediction.csv
 	- Output: CSA in a CSV file


6. 'statistics.py'

	Set the proj_dir, raw_img_dir, raw_seg_dir, Slice Prediction CSV, and output_dir directories before executing the code. 
	This script generates the Cross-Sectional Area (CSA) of the C3 Skeletal Muscle Mass from the auto-segmented masks.
   	- Input#1 : Auto segmentation files
 	- Input#2: Manual segmentation files of test data
 	- Input#3: C3_Top_Slice_Prediction.csv
 	- Output: CSA in a CSV file


7. 'visualize.py'

	Set the proj_dir, raw_img_dir, raw_seg_dir, Slice Prediction CSV, and output_dir directories before executing the code. 
	This script generates the masks with contours for easy visualization. 
   	- Input#1 : Auto segmentation files
 	- Input#2: Manual segmentation files of test data
 	- Input#3: C3_Top_Slice_Prediction.csv
 	- Output: CSA in a CSV file


8. 'clinical.py'

	Set the proj_dir, raw_img_dir, raw_seg_dir, Slice Prediction CSV, and output_dir directories before executing the code. 
	This script generates the C3 Skeletal Muscle Index (SMI) and translates that to the corresponding L3 Skeletal Muscle Index (SMI).
   	- Input#1 : Auto segmentation files
 	- Input#2: Manual segmentation files of test data
 	- Input#3: C3_Top_Slice_Prediction.csv
 	- Output: CSA in a CSV file
