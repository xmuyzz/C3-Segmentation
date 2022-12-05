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

#### NOTE: ensure the correct lirabry path
from scripts.interpolate import interpolate
from scripts.data_util import get_arr_from_nrrd, get_bbox, generate_sitk_obj_from_npy_array
from scripts.crop import crop_top_img_only
from scripts.resize_3d import resize_3d


def preprocess(img_raw_dir, img_crop_dir):
    img_dirs = [i for i in sorted(glob.glob(img_raw_dir + '/*nrrd'))]
    print(img_dirs)
    img_ids = []
    bad_ids = []
    bad_scans = []
    count = 0
    for img_dir in img_dirs:
        img_id = img_dir.split('/')[-1].split('.')[0]
        img_ids.append(img_id)
        count += 1
        print(count, img_id)
        # load img and seg
        img = sitk.ReadImage(img_dir, sitk.sitkFloat32)
        # --- crop full body scan ---
        z_img = img.GetSize()[2]
        print("raw image shape and spacing")
        print(img.GetSize())
        print(img.GetSpacing())
        spacing = img.GetSpacing()[-1]
        if z_img < 10:
            print('This is an incomplete scan!')
            bad_scans.append(img_id)
        else:
#            try:
            # --- interpolation for image and seg to 1x1x3 ---
            # interpolate images
            print('interpolate')
            img_interp = interpolate(
                patient_id=img_id,
                path_to_nrrd=img_dir,
                interpolation_type='linear', #"linear" for image
                new_spacing=(1, 1, spacing),
                return_type='sitk_obj',
                output_dir='',
                image_format='nrrd')
            print("shape after re-spacing")
            print(img_interp.GetSize())
            print('cropping')
            crop_top_img_only(
                patient_id=img_id,
                img=img_interp,
                crop_shape=(256, 256, z_img),
                return_type='sitk_object',
                output_dir=img_crop_dir,
                image_format='nrrd')
            print('successfully crop!')
#            except Exception as e:
#                bad_ids.append(img_id)
#                print(img_id, e)
    print('bad ids:', bad_ids)
    print('incomplete scans:', bad_scans)


if __name__ == '__main__':

    prepross(proj_dir)



