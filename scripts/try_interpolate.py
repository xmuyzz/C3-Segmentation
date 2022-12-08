#from google.colab import drive
#drive.mount('/content/drive')
import glob, os, functools
import numpy as np
import pandas as pd
import SimpleITK as sitk
import operator
from scipy import ndimage
from SimpleITK.extra import GetArrayFromImage
from scipy import ndimage
#import cv2
import matplotlib as plt
from interpolate import interpolate
from crop_image import crop_top, crop_top_image_only, crop_full_body
from registration import nrrd_reg_rigid


def main():
    proj_dir = '/mnt/kannlab_rfa/Zezhong/c3_segmentation'
    raw_seg_dir = proj_dir + '/output/pred'
    raw_img_dir = proj_dir + '/data/segmentation/img' 
    crop_seg_dir = proj_dir + '/test/test_seg'
    crop_img_dir = proj_dir + '/test/test_img'
    if not os.path.exists(crop_seg_dir):
        os.makedirs(crop_seg_dir)
    if not os.path.exists(crop_img_dir):
        os.makedirs(crop_img_dir)
    img_dirs = [i for i in sorted(glob.glob(raw_img_dir + '/*nrrd'))]
    seg_dirs = [i for i in sorted(glob.glob(raw_seg_dir + '/*nrrd'))]
    img_ids = []
    count = 0
    img_ids = []
    bad_ids = []
    bad_scans = []
    count = 0
    # get register template
    fixed_img = sitk.ReadImage(img_dirs[0], sitk.sitkFloat32)
    for img_dir in img_dirs:
        img_id = img_dir.split('/')[-1].split('.')[0]
        seg_dir = raw_seg_dir + '/' + img_id + '.nrrd'
        img_ids.append(img_id)
        count += 1
        print(count, img_id)
        # load img and seg
        img = sitk.ReadImage(img_dir, sitk.sitkFloat32)
        seg = sitk.ReadImage(seg_dir, sitk.sitkFloat32)
        # --- crop full body scan ---
        z_img = img.GetSize()[2]
        z_seg = seg.GetSize()[2]
        if z_img < 105:
            print('This is an incomplete scan!')
            bad_scans.append(img_id)
        else:
            if z_img > 200:
                img = crop_full_body(img, int(z_img * 0.65))
                seg = crop_full_body(seg, int(z_seg * 0.65))
            try:
                # --- interpolation for image and seg to 1x1x3 ---
                # interpolate images
                print('interplolate')
                img_interp = interpolate(
                    patient_id=img_id, 
                    path_to_nrrd=img_dir, 
                    interpolation_type='linear', #"linear" for image
                    new_spacing=(1, 1, 3), 
                    return_type='sitk_obj', 
                    output_dir='',
                    image_format='nrrd')
                # interpolate segs
                seg_interp = interpolate(
                    patient_id=img_id, 
                    path_to_nrrd=seg_dir, 
                    interpolation_type='nearest_neighbor', # nearest neighbor for label
                    new_spacing=(1, 1, 3), 
                    return_type='sitk_obj', 
                    output_dir='',
                    image_format='nrrd')
#                print('register')
#                reg_img, fixed_img, moving_img, final_transform = nrrd_reg_rigid(
#                    patient_id=img_id,
#                    moving_img=img_interp,
#                    output_dir='',
#                    fixed_img=fixed_img,
#                    image_format='nrrd')
#                # register segmentations
#                reg_seg = sitk.Resample(
#                    seg_interp,
#                    fixed_img,
#                    final_transform,
#                    sitk.sitkNearestNeighbor,
#                    0.0,
#                    moving_img.GetPixelID())
                # --- crop ---
                print('cropping')
                crop_top(
                    patient_id=img_id,
                    img=img_interp,
                    seg=seg_interp,
                    crop_shape=(256, 256, 96),
                    return_type='sitk_object',
                    output_img_dir=crop_img_dir,
                    output_seg_dir=crop_seg_dir,
                    image_format='nrrd')
            except Exception as e:
                bad_ids.append(img_id)
                print(img_id, e)
    print('bad ids:', bad_ids)
    print('incomplete scans:', bad_scans)

if __name__ == '__main__':

    main()



