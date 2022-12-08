import os
import operator
import numpy as np
import SimpleITK as sitk
from scripts.data_util import get_arr_from_nrrd, get_bbox, generate_sitk_obj_from_npy_array
#from scipy.ndimage import sobel, generic_gradient_magnitude
from scipy import ndimage
from SimpleITK.extra import GetArrayFromImage
from scipy import ndimage
#import cv2
import matplotlib as plt
from scripts.resize_3d import resize_3d
    

def crop_top_img_only(patient_id, img, crop_shape, return_type, output_dir, image_format):
    """
    Will center the image and crop top of image after it has been registered.
    Args:
        dataset (str): Name of dataset.
        patient_id (str): Unique patient id.
        path_to_image_nrrd (str): Path to image nrrd file.
        path_to_label_nrrd (str): Path to label nrrd file.
        crop_shape (list) shape to save cropped image  (x, y, z)
        return_type (str): Either 'sitk_object' or 'numpy_array'.
        output_folder_image (str) path to folder to save image nrrd
        output_folder_label (str) path to folder to save label nrrd
    Returns:
        Either a sitk image object or a numpy array derived from it (depending on 'return_type') of both image and label.
    Raises:
        Exception if an error occurs.
    """

    # get image, arr, and spacing
    img_arr = sitk.GetArrayFromImage(img)
    img_origin = img.GetOrigin()
    img_spacing = img.GetSpacing()
    c, y, x = img_arr.shape
    ## Get center of mass to center the crop in Y plane
    mask_arr = np.copy(img_arr) 
    mask_arr[mask_arr > -500] = 1
    mask_arr[mask_arr <= -500] = 0
    mask_arr[mask_arr >= -500] = 1 
    #print("mask_arr min and max:", np.amin(mask_arr), np.amax(mask_arr))
    centermass = ndimage.measurements.center_of_mass(mask_arr) # z,x,y   
    cpoint = c - crop_shape[2]//2
    #print("cpoint, ", cpoint)
    centermass = ndimage.measurements.center_of_mass(mask_arr[cpoint, :, :])   
    #print("center of mass: ", centermass)
    startx = int(centermass[0] - crop_shape[0]//2)
    starty = int(centermass[1] - crop_shape[1]//2)      
    #startx = x//2 - crop_shape[0]//2       
    #starty = y//2 - crop_shape[1]//2
    startz = int(c - crop_shape[2])
    #print("start X, Y, Z: ", startx, starty, startz)
    
    # cut bottom slices
    #image_arr = image_arr[30:, :, :]
    #-----normalize CT data signals-------
    norm_type = 'np_clip'
    #image_arr[image_arr <= -1024] = -1024
    ## strip skull, skull UHI = ~700
    #image_arr[image_arr > 700] = 0
    ## normalize UHI to 0 - 1, all signlas outside of [0, 1] will be 0;
    if norm_type == 'np_interp':
        img_arr = np.interp(img_arr, [-200, 200], [0, 1])
    elif norm_type == 'np_clip':
        #img_arr = np.clip(img_arr, a_min=-200, a_max=200)
        img_arr = np.clip(img_arr, a_min=-175, a_max=275)
        MAX, MIN = img_arr.max(), img_arr.min()
        img_arr = (img_arr - MIN) / (MAX - MIN)

    if startz < 0:
        img_arr = np.pad(
            img_arr,
            ((abs(startz)//2, abs(startz)//2), (0, 0), (0, 0)), 
            'constant', 
            constant_values=-1024)
        img_arr_crop = img_arr[
            0:crop_shape[2], starty:starty + crop_shape[1], startx:startx + crop_shape[0]]
    elif startx < 0 :
        img_arr_crop = img_arr[0:crop_shape[2], 0:y, 0:x]
    else:
        img_arr_crop = img_arr[
            0:crop_shape[2], starty:starty + crop_shape[1], startx:startx + crop_shape[0]]
#    if img_arr_crop.shape[0] < crop_shape[2]:
#        print("initial cropped image shape too small:", img_arr_crop.shape)
#        print(crop_shape[2], img_arr_crop.shape[0])
#        img_arr_crop = np.pad(
#            img_arr_crop,
#            ((int(crop_shape[2] - img_arr_crop.shape[0]), 0), (0,0), (0,0)),
#            'constant',
#            constant_values=-1024)
#        print("padded size: ", img_arr_crop.shape)
    #print('Returning bottom rows')
    save_dir = output_dir + '/' + patient_id + '.' + image_format
    img_sitk = sitk.GetImageFromArray(img_arr_crop)
    # resize img back to 512x512
    resize_shape = (512, 512, img_sitk.GetSize()[2])
    img_sitk.SetSpacing(img_spacing)
    img_sitk.SetOrigin(img_origin)
    img_sitk = resize_3d(img_sitk, sitk.sitkLinear, resize_shape)
    # save nrrd
    img_sitk.SetSpacing(img_spacing)
    img_sitk.SetOrigin(img_origin)
    writer = sitk.ImageFileWriter()
    writer.SetFileName(save_dir)
    writer.SetUseCompression(True)
    writer.Execute(img_sitk)


