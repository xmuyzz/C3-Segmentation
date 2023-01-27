import os
import SimpleITK as sitk
import numpy as np
from unet import get_unet_2D
from image_processing.image_window import get_image_path_by_id, remove_arm_area
from image_processing.get_sitk_from_array import write_sitk_from_array_by_template
import pandas as pd


def test_segmentation(img_dir, model_weight_path, slice_csv_path, output_dir):
    
    # load model and weights
    model = get_unet_2D(2, (512, 512, 1), num_convs=2, activation='relu',
            compression_channels=[16, 32, 64, 128, 256, 512],
            decompression_channels=[256, 128, 64, 32, 16])
    model.load_weights(model_weight_path)
    
    # load data for prediction
    df = pd.read_csv(slice_csv_path)
    IDs = []
    errors = []
    i = 0
    for ID, c3_slice in zip(df['ID'], df['pred_slice']):    
        i += 1
        print(i, ID)
        save_path = output_dir + '/' + str(ID) + '.nrrd'
        img_path = img_dir + '/' + str(ID) + '.nrrd'
        try:
            img_sitk = sitk.ReadImage(img_path)
            img_arr_3d = sitk.GetArrayFromImage(img_sitk)
            im_xy_size = img_arr_3d.shape[1]
            c3_slice = int(c3_slice)
            print('c3 slice:', c3_slice)
            img_arr = sitk.GetArrayFromImage(img_sitk)[c3_slice, :, :].reshape(1, 512, 512, 1) 
            # normalize data
            #img_arr = np.clip(img_arr, a_min=-175, a_max=275)
            #img_arr = np.clip(img_arr, a_min=-200, a_max=200)
            #MAX, MIN = img_arr.max(), img_arr.min()
            #img_arr = (img_arr - MIN) / (MAX - MIN)

            img_arr_2d = sitk.GetArrayFromImage(img_sitk)[c3_slice, :, :]
            target_area = remove_arm_area(img_arr_2d)
            pred_arr = model.predict(img_arr)
            softmax_threshold = 0.5
            muscle_seg = (pred_arr[:, :, :, 1] >= softmax_threshold) * 1.0 * target_area           
            pred_arr_2d = muscle_seg 
            pred_arr_3d = np.zeros(img_arr_3d.shape)
            pred_arr_3d[c3_slice, :, :] = pred_arr_2d
            #print(img_arr_2d.shape)
            #print(pred_arr_2d.shape)
            write_sitk_from_array_by_template(pred_arr_3d, img_sitk, save_path)
        except Exception as e:
            print(ID, e)
            IDs.append(ID)
            errors.append(e)
    print(IDs)
    print(errors)


def main():
    proj_dir = '/mnt/kannlab_rfa/Zezhong/c3_segmentation'    
    img_dir = proj_dir + '/internal_test/prepro_img'
    seg_dir = proj_dir + '/internal_test/prepro_seg'
    model_path = proj_dir + '/model/test/C3_Top_Segmentation_Model_Weight.hdf5'
    slice_csv_path = proj_dir + '/internal_test/slice_model/slice_tot.csv'
    output_dir = proj_dir + '/internal_test/pred_seg'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    test_segmentation(
        img_dir=img_dir,
        model_weight_path=model_path,
        slice_csv_path=slice_csv_path,
        output_dir=output_dir)

if __name__ == '__main__':

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    main()