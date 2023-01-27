import numpy as np
import os
import glob
import shutil
#import pydicom as dicom
import pandas as pd
import SimpleITK as sitk

def get_slice():
    
    proj_dir = '/mnt/kannlab_rfa/Zezhong/c3_segmentation/data'
    #data_path = proj_dir + '/train_data/raw_data/seg/MDA0001.nrrd'
    data_dir = proj_dir + '/train_data/raw_data/seg'
    for img_dir in sorted(glob.glob(data_dir + '/*nrrd')):
        img = sitk.ReadImage(img_dir)
        arr = sitk.GetArrayFromImage(img)
        #w = np.any(arr, axis=(1, 2))
        #print(w)
        w1, w2 = np.where(arr)[0][[0, -1]]
        print(w1)


def move_file():
    proj_dir = '/mnt/kannlab_rfa/Zezhong/c3_segmentation/inference'
    img_dir1 = proj_dir + '/crop_resize_img'
    img_dir2 = proj_dir + '/crop_resize_img2'
    for img_path in glob.glob(img_dir2 + '/*nrrd'):
        if img_path.split('/')[-1].split('.')[-2] == 'nrrd':
            ID = img_path.split('/')[-1].split('.')[0]
            print(ID)
            save_path = img_dir1 + '/' + ID + '.nrrd'
            shutil.move(img_path, save_path)

def dcm_header():
    proj_dir = '/mnt/kannlab_rfa/Ben/HN_NonOPC_Dicom_Export'
    proj_dir = '/mnt/kannlab_rfa/Zezhong/HeadNeck/data/OPC2/dcm'
    case = '10068290765_1172522468_HN'
    dcm = 'CT.1.2.840.113619.2.55.3.3752513132.5591.1172522468.976.1.dcm'
    dcm_path = proj_dir + '/' + case + '/' + dcm
    ds = dicom.read_file(dcm_path, force=True)
    #print(ds)
    print(ds[0x0008, 0x0020])


def get_names():
    proj_dir = '/mnt/kannlab_rfa/Zezhong/c3_segmentation/data/slice_selection'
    df = pd.read_csv(proj_dir + '/C3_slice_selection.csv', index_col=0)
    IDs = []
    for i, pat_id in enumerate(df['patient_id']):
        ID = pat_id.split('_')[1].split('-')[2]
        print(i, ID)
        ID = 'MDA' + ID
        IDs.append(ID)
    df['ID'] = IDs
    df.to_csv(proj_dir + '/C3_slice_sum.csv', index=False)
        

def get_test_data():
    proj_dir = '/mnt/kannlab_rfa/Zezhong/c3_segmentation/data'
    img_dir = proj_dir + '/train_data/raw_data/img'
    seg_dir = proj_dir + '/train_data/raw_data/seg'
    save_img_dir = proj_dir + '/train_data/test_img'
    save_seg_dir = proj_dir + '/train_data/test_seg'
    if not os.path.exists(save_img_dir):
        os.makedirs(save_img_dir)
    if not os.path.exists(save_seg_dir):
        os.makedirs(save_seg_dir)
    df = pd.read_csv(proj_dir + '/slice_selection/C3_slice_sum.csv', index_col=0)
    df = df[df['Datatype']=='test']
    for i, ID in enumerate(df['ID']):
        print(i, ID)
        img_path = img_dir + '/' + ID + '.nrrd'
        save_img_path = save_img_dir + '/' + ID + '.nrrd'
        seg_path = seg_dir + '/' + ID + '.nii.gz'
        save_seg_path = save_seg_dir + '/' + ID + '.nii.gz'
        shutil.copyfile(img_path, save_img_path)
        shutil.copyfile(seg_path, save_seg_path)


def nii_to_nrrd():
    proj_dir = '/mnt/kannlab_rfa/Zezhong/c3_segmentation/data/train_data'
    seg_dir = proj_dir + '/raw_seg'
    for seg_path in glob.glob(seg_dir + '/*nii.gz'):
        ID = seg_path.split('/')[-1].split('.')[0]
        print(ID)
        save_path = seg_dir + '/' + ID + '.nrrd'
        if not os.path.exists(save_path):
            seg = sitk.ReadImage(seg_path)
            seg.SetSpacing(seg.GetSpacing())
            seg.SetOrigin(seg.GetOrigin())
            writer = sitk.ImageFileWriter()
            writer.SetFileName(save_path)
            writer.SetUseCompression(True)
            writer.Execute(seg)

def rename():
    proj_dir = /mnt/kannlab_rfa/Zezhong/c3_segmentation/internal_test'
    img_dir = proj_dir + '/yash_img'
    seg_dir = proj_dir + '/yash_seg'
    for i, img_path in enumerate(img_dir):
        ID = img_dir.split('_')[1].split('-')[2]
        print(i, ID)
        save_path = img_dir + '/' + ID + '.nrrd'
        os.rename(img_path, save_path)
    for i, seg_path in enumerate(seg_dir):
        ID = seg_dir.split('_')[1].split('-')[2]
        print(i, ID)
        save_path = seg_dir + '/' + ID + '.nrrd'
        os.rename(seg_path, save_path)
        
if __name__ == '__main__':
    #get_slice()
    #move_file()
    #get_names()
    #get_test_data()
    #nii_to_nrrd()
    rename()





