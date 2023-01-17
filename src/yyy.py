import numpy as np
import os
import glob
import shutil


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
            
if __name__ == '__main__':
    #get_slice()
    move_file()
