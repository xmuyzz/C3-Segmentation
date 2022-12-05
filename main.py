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
from scripts.preprocess import preprocess
from scripts.image_processing.slice_area_density import get_c3_slice_area, get_c3_slice_density


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


def preprocess_data(proj_dir, dataset):
    """
    Test the Slice Selction Model
    Args:
        Input Scans -- nrrd files
        Model -- C3_Top_Selection_Model_Weight.hdf5 
        Output -- C3_Top_Slice_Prediction.csv' 
    """
    
    # preprocess data
    if dataset == 'OPC':
        folder = 'BWH'
    elif dataset == 'NonOPC':
        folder = 'NonOPC'
    raw_img_dir = proj_dir + '/HeadNeck/data/' + folder + '/raw_img'
    crop_img_dir = proj_dir + '/HeadNeck/data/' + folder + '/crop_img'
    if not os.path.exists(crop_img_dir):
        os.makedirs(crop_img_dir)
    print('--- C3 segmentation ---')
    preprocess(raw_img_dir, crop_img_dir)


def save_img_slice(proj_dir, dataset):
    if dataset == 'OPC':
        csv = 'OPC_C3_top_slice_pred.csv'
        csv_path = proj_dir + '/c3_segmentation/output/' + csv
        img_dir = proj_dir + '/HeadNeck/data/BWH/crop_img'
        seg_dir = proj_dir + '/c3_segmentation/output/OPC'
    elif dataset == 'NonOPC':
        csv = 'NonOPC_C3_top_slice_pred.csv'
        csv_path = proj_dir + '/c3_segmentation/output/' + csv
        img_dir = proj_dir + '/HeadNeck/data/NonOPC/crop_img'
        seg_dir = proj_dir + '/c3_segmentation/output/NonOPC'
    save_img_dir = proj_dir + '/c3_segmentation/visualize/img'
    save_seg_dir = proj_dir + '/c3_segmentation/visualize/seg'
    if not os.path.exists(save_img_dir):
        os.makedirs(save_img_dir)
    if not os.path.exists(save_seg_dir):
        os.makedirs(save_seg_dir)
    for dataset in ['OPC', 'NonOPC']:
        df = pd.read_csv(csv_path)
        count = 0
        for ID, Slice in zip(df['patient_id'], df['C3_Predict_slice']):
            count += 1
            print(count, ID)
            for data_dir, save_dir in zip([img_dir, seg_dir], [save_img_dir, save_seg_dir]):
                data_path = data_dir + '/' + ID + '.nrrd'
                nrrd = sitk.ReadImage(data_path)
                arr = sitk.GetArrayFromImage(nrrd)
                arr_slice = arr[Slice, :, :]
                save_path = save_dir + '/' + ID + '.nrrd'
                img_sitk = sitk.GetImageFromArray(arr_slice)
                img_sitk.SetSpacing(nrrd.GetSpacing())
                img_sitk.SetOrigin(nrrd.GetOrigin())
                writer = sitk.ImageFileWriter()
                writer.SetFileName(save_path)
                writer.SetUseCompression(True)
                writer.Execute(img_sitk)


def segmentation(proj_dir, dataset):
    # preprocess data
    if dataset == 'OPC':
        folder = 'BWH'
    elif dataset == 'NonOPC':
        folder = 'NonOPC'
    crop_img_dir = proj_dir + '/HeadNeck/data/' + folder + '/crop_img'
    # segmentation
    seg_model = 'C3_Top_Segmentation_Model_Weight.hdf5'
    seg_model_path = proj_dir + '/c3_segmentation/model/test/' + seg_model
    slice_csv = dataset + '_C3_top_slice_pred.csv'
    slice_csv_path = proj_dir + '/c3_segmentation/output/' + slice_csv
    output_seg_dir = proj_dir + '/c3_segmentation/output/' + dataset
    if not os.path.exists(output_seg_dir):
        os.makedirs(output_seg_dir)
    print('--- C3 segmentation ---')
    test_segmentation(
        image_dir=crop_img_dir,
        model_weight_path=seg_model_path,
        l3_slice_csv_path=slice_csv_path,
        output_dir=output_seg_dir)


def get_area(proj_dir, dataset):

    slice_csv = dataset + '_C3_top_slice_pred.csv'
    area_csv = dataset + '_C3_body_comp_area_density.csv'
    if dataset == 'OPC':
        folder = 'BWH'
    elif dataset == 'NonOPC':
        folder = 'NonOPC'
    crop_img_dir = proj_dir + '/HeadNeck/data/' + folder + '/crop_img'
    slice_csv_path = proj_dir + '/c3_segmentation/output/' + slice_csv
    area_csv_path = proj_dir + '/c3_segmentation/output/' + area_csv
    output_seg_dir = proj_dir + '/c3_segmentation/output/' + dataset

    print('--- get C3 muscle cross sectional area ---')
    df_infer = pd.read_csv(slice_csv_path)
    df_init = pd.DataFrame()
    IDs = []
    for idx in range(df_infer.shape[0]):
        try:
            ID = str(df_infer.iloc[idx, 1])
            c3_slice_auto = df_infer.iloc[idx, 2]
            muscle_area, sfat_area, vfat_area = get_c3_slice_area(
                patient_id=ID, 
                c3_slice=c3_slice_auto, 
                seg_dir=output_seg_dir)
            muscle_density, sfat_density, vfat_density = get_c3_slice_density(
                patient_id=ID, 
                c3_slice=c3_slice_auto, 
                seg_dir=output_seg_dir, 
                img_dir=crop_img_dir)
            #Data Frame rows for writing into a CSV File
            df_inter1 = pd.DataFrame({
                'patient_id': ID,
                'muscle_auto_segmentation_area': round(muscle_area, 2),
                'muscle_auto_edensity': round(muscle_density, 2)
                }, index=[0])
            df_init = df_init.append(df_inter1)
            df_init.to_csv(area_csv_path)
            print(idx,'th', ID, 'writen to', area_csv_path)
        except Exception as e:
            print(ID, e)
            IDs.append(ID)
    print('bad data:', IDs)

if __name__ == '__main__':

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    warnings.filterwarnings('ignore')
    proj_dir = '/mnt/kannlab_rfa/Zezhong'
    dataset = 'NonOPC'
    
    #segmentation(proj_dir, dataset)
    #get_area(proj_dir, dataset)
    save_img_slice(proj_dir, dataset)













