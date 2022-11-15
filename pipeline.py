import argparse
import warnings
import os 
from scripts.infer_selection import test_slice_selection
import pandas as pd
from scripts.image_processing.image_window import get_image_path_by_id, apply_window
from scripts.image_processing.slice_array_from_nifty import get_C3_seg_array_by_id
import SimpleITK as sitk
import numpy as np
from pprint import pprint
from scripts.infer_segmentation import test_segmentation
from scripts.image_processing.slice_area_density import get_c3_slice_area, get_c3_slice_density


def segmentation(proj_dir):
    """
    Test the Slice Selction Model
    Args:
        Input Scans -- nrrd files
        Model -- C3_Top_Selection_Model_Weight.hdf5 
        Output -- C3_Top_Slice_Prediction.csv' 
    """

    slice_model = 'C3_Top_Selection_Model_Weight.hdf5'
    seg_model = 'C3_Top_Segmentation_Model_Weight.hdf5'
    slice_csv = 'C3_top_slice_prediction.csv'
    
    img_dir = proj_dir + '/HeadNeck/data/NonOPC/raw_img'
    slice_model_path = proj_dir + '/c3_segmentation/model/test/' + slice_model
    seg_model_path = proj_dir + '/c3_segmentation/model/test/' + seg_model
    slice_csv_path = proj_dir + '/c3_segmentation/output/' + slice_csv
    output_seg_dir = proj_dir + '/c3_segmentation/output/seg_pred'
    if not os.path.exists(output_seg_dir):
        os.makedirs(output_seg_dir)
   
    # slice selection model
    print('--- slice selection ---')
    test_slice_selection(
        image_dir=img_dir, 
        model_weight_path=slice_model_path, 
        csv_write_path=slice_csv_path)

    # segmentation model
    print('--- C3 segmentation ---')
    test_segmentation(
        image_dir=img_dir, 
        model_weight_path=seg_model_path, 
        l3_slice_csv_path=slice_csv_path, 
        output_dir=output_seg_dir)


def get_area(proj_dir):

    slice_csv = 'C3_top_slice_prediction.csv'
    area_csv = 'C3_body_comp_area_density.csv'

    img_dir = proj_dir + '/HeadNeck/data/NonOPC/raw_img'
    slice_csv_path = proj_dir + '/c3_segmentation/output/' + slice_csv
    area_csv_path = proj_dir + '/c3_segmentation/output/' + area_csv
    output_seg_dir = proj_dir + '/c3_segmentation/output/seg_pred'

    # get C3 muscle cross sectional area for each of the scans
    print('--- get C3 muscle cross sectional area ---')
    df_infer = pd.read_csv(slice_csv_path)
    df_init = pd.DataFrame()
    for idx in range(df_infer.shape[0]):
        ID = str(df_infer.iloc[idx, 1])
        c3_slice_auto = df_infer.iloc[idx, 2]
        #img_path = get_image_path_by_id(patient_id=ID, image_dir=img_dir)
        #seg_path = get_image_path_by_id(patient_id=ID, image_dir=output_seg_dir)
        img_path = img_dir + '/' + ID + '.nrrd'
        seg_path = output_seg_dir + '/' + ID + '.nrrd'
        if os.path.exists(img_path) and os.path.exists(seg_path):
            muscle_area, sfat_area, vfat_area = get_c3_slice_area(
                patient_id=ID, 
                c3_slice=c3_slice_auto, 
                seg_dir=output_seg_dir)
            muscle_density, sfat_density, vfat_density = get_c3_slice_density(
                patient_id=ID, 
                c3_slice=c3_slice_auto, 
                seg_dir=output_seg_dir, 
                img_dir=img_dir)
            #Data Frame rows for writing into a CSV File
            df_inter1 = pd.DataFrame({
                'patient_id': ID,
                'muscle_auto_segmentation_area': round(muscle_area, 2),
                'muscle_auto_edensity': round(muscle_density, 2)
                }, index=[0])
            df_init = df_init.append(df_inter1)
            df_init.to_csv(area_csv_path)
            print(idx,'th', ID, 'writen to', area_csv_path)


if __name__ == '__main__':

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    warnings.filterwarnings('ignore')
    proj_dir = '/mnt/kannlab_rfa/Zezhong'
    
    segmentation(proj_dir)
    get_area(proj_dir)














