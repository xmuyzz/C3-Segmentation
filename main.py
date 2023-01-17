import argparse
import warnings
import os 
import pandas as pd
import SimpleITK as sitk
import numpy as np
from src.infer_segmentation import test_segmentation
from src.infer_slice_selection import test_slice_selection


def slice_selection(proj_dir, dataset):
    """
    Test the Slice Selction Model
    Args:
        Input Scans -- nrrd files
        Model -- C3_Top_Selection_Model_Weight.hdf5 
        Output -- C3_Top_Slice_Prediction.csv' 
    """
    if dataset == 'OPC':
        folder = 'BWH'
    elif dataset == 'NonOPC':
        folder = 'NonOPC'
    raw_img_dir = proj_dir + '/HeadNeck/data/' + folder + '/raw_img'
    slice_model = 'C3_Top_Selection_Model_Weight.hdf5'
    slice_model_path = proj_dir + '/c3_segmentation/model/test/' + slice_model
    slice_csv = dataset + '_C3_top_slice_pred.csv'
    slice_csv_path = proj_dir + '/c3_segmentation/output/' + slice_csv 
    print('--- slice selection ---')
    test_slice_selection(
        image_dir=raw_img_dir, 
        model_weight_path=slice_model_path, 
        csv_write_path=slice_csv_path)


def segmentation():
    proj_dir = '/mnt/kannlab_rfa/Zezhong/c3_segmentation'    
    img_dir = proj_dir + '/inference/crop_resize_img2'
    model_path = proj_dir + '/model/test/C3_Top_Segmentation_Model_Weight.hdf5'
    slice_csv_path = proj_dir + '/clinical/C3_top_slice_pred.csv'
    output_dir = proj_dir + '/inference/pred_new'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    print('--- C3 segmentation ---')
    test_segmentation(
        image_dir=img_dir,
        model_weight_path=model_path,
        l3_slice_csv_path=slice_csv_path,
        output_dir=output_dir)


if __name__ == '__main__':

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    warnings.filterwarnings('ignore')

    segmentation()












