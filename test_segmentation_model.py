import argparse
import warnings
import os 
import pandas as pd
import SimpleITK as sitk
import numpy as np
from src.infer_segmentation import test_segmentation
from src.infer_slice_selection import test_slice_selection


def segmentation():
    proj_dir = '/mnt/kannlab_rfa/Zezhong/c3_segmentation'    
    img_dir = proj_dir + '/internal_test/prepro_img'
    seg_dir = proj_dir + '/internal_test/prepro_seg'
    model_path = proj_dir + '/model/test/C3_Top_Segmentation_Model_Weight.hdf5'
    slice_csv_path = proj_dir + '/internal_test/slice_model/slice_tot.csv'
    output_dir = proj_dir + '/internal_test/segmentation_model/preds'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    test_segmentation(
        img_dir=img_dir,
        model_weight_path=model_path,
        slice_csv_path=slice_csv_path,
        output_dir=output_dir)

if __name__ == '__main__':

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    warnings.filterwarnings('ignore')

    segmentation()












