import numpy as np
import os
import pandas as pd
import glob
from PIL import Image, ImageOps
import SimpleITK as sitk
import matplotlib.pyplot as plt
import cv2


def draw_contour():
    """get segmentation and image fusion in JPG format
    """
    proj_dir = '/mnt/kannlab_rfa/Zezhong/c3_segmentation/visualize'
    if not os.path.exists(proj_dir + '/C3_contour'):
        os.makedirs(proj_dir + '/C3_contour')
    img_paths = [i for i in sorted(glob.glob(proj_dir + '/img/*nrrd'))]
    seg_paths = [i for i in sorted(glob.glob(proj_dir + '/seg/*nrrd'))]
    count = 0
    IDs = []
    for img_path, seg_path in zip(img_paths, seg_paths):
        ID = img_path.split('/')[-1].split('.')[0]
        count += 1
        print(count, ID)
        IDs.append(ID)
        nrrd_img = sitk.ReadImage(img_path)
        arr_img = sitk.GetArrayFromImage(nrrd_img)
        nrrd_seg = sitk.ReadImage(seg_path)
        arr_seg = sitk.GetArrayFromImage(nrrd_seg)
        # generate contour with CV2
        img = np.uint8(arr_img*255)
        seg = np.uint8(arr_seg*255)
        contour, hierarchy = cv2.findContours(seg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        main = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.drawContours(
            image=main, 
            contours=contour, 
            contourIdx=-1, 
            color=(0, 0, 255), 
            thickness=1,
            lineType=16)
        cv2.imwrite(proj_dir + '/C3_contour/' + ID + '.png', main) 
    df = pd.DataFrame({'ID': IDs})
    df.to_csv(proj_dir + '/patient_list.csv', index=False)


def save_contour():
    proj_dir = '/mnt/kannlab_rfa/Zezhong/c3_segmentation'
    csv_path = proj_dir + '/output/C3_top_slice_pred.csv'
    img_dir = proj_dir + '/data/segmentation/img'
    seg_dir = proj_dir + '/output/pred'
    save_dir = proj_dir + '/visualize/C3_contour'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    df = pd.read_csv(csv_path)
    count = 0
    bad_data = []
    IDs = []
    for ID, Slice in zip(df['patient_id'], df['C3_Predict_slice']):
        count += 1
        print(count, ID)
        IDs.append(ID)
        try:
            img_path = img_dir + '/' + ID + '.nrrd'
            seg_path = seg_dir + '/' + ID + '.nrrd'
            save_path = save_dir + '/' + ID + '.png'
            img_nrrd = sitk.ReadImage(img_path)
            img_arr = sitk.GetArrayFromImage(img_nrrd)
            seg_nrrd = sitk.ReadImage(seg_path)
            seg_arr = sitk.GetArrayFromImage(seg_nrrd)
            img_slice = img_arr[Slice, :, :]
            seg_slice = seg_arr[Slice, :, :]
            # generate contour with CV2
            img = np.uint8(img_slice*255)
            seg = np.uint8(seg_slice*255)
            contour, hierarchy = cv2.findContours(seg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            main = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cv2.drawContours(
                image=main,
                contours=contour,
                contourIdx=-1,
                color=(0, 0, 255),
                thickness=1,
                lineType=16)
            cv2.imwrite(save_path, main)
        except Exception as e:
            print(ID)
            bad_data.append(ID)
    print('bad_data:', bad_data)
    df = pd.DataFrame({'ID': IDs})
    df.to_csv(proj_dir + '/patient_list.csv', index=False)


def save_slice():
    proj_dir = '/mnt/kannlab_rfa/Zezhong/c3_segmentation'
    csv_path = proj_dir + '/output/C3_top_slice_pred.csv'
    img_dir = proj_dir + '/data/segmentation/img'
    seg_dir = proj_dir + '/output/pred'
    save_img_dir = proj_dir + '/visualize/img'
    save_seg_dir = proj_dir + '/visualize/seg'
    if not os.path.exists(save_img_dir):
        os.makedirs(save_img_dir)
    if not os.path.exists(save_seg_dir):
        os.makedirs(save_seg_dir)
    df = pd.read_csv(csv_path)
    count = 0
    bad_data = []
    for ID, Slice in zip(df['patient_id'], df['C3_Predict_slice']):
        count += 1
        print(count, ID)
        for data_dir, save_dir in zip([img_dir, seg_dir], [save_img_dir, save_seg_dir]):
            try:
                data_path = data_dir + '/' + ID + '.nrrd'
                save_path = save_dir + '/' + ID + '.nrrd'
                if os.path.exists(save_path):
                    print('data exists')
                else:
                    nrrd = sitk.ReadImage(data_path)
                    arr = sitk.GetArrayFromImage(nrrd)
                    arr_slice = arr[Slice, :, :]
                    img_sitk = sitk.GetImageFromArray(arr_slice)
                    img_sitk.SetSpacing(nrrd.GetSpacing())
                    img_sitk.SetOrigin(nrrd.GetOrigin())
                    writer = sitk.ImageFileWriter()
                    writer.SetFileName(save_path)
                    writer.SetUseCompression(True)
                    writer.Execute(img_sitk)
            except Exception as e:
                print(ID)
                bad_data.append(ID)
    print('bad_data:', bad_data)


if __name__ == '__main__':

    #save_img_slice()
    #draw_contour()
    save_contour()



