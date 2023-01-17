import os
import pandas as pd
import SimpleITK as sitk
import numpy as np
from src.slice_area_density import get_c3_slice_area, get_c3_slice_density


def get_CSA(proj_dir):
    """get C3 muscle area and density
    """
    img_dir = proj_dir + '/c3_segmentation/inference/crop_resize_img'
    seg_dir = proj_dir + '/c3_segmentation/inference/pred_new'
    df = pd.read_csv(proj_dir + '/c3_segmentation/inference/files/C3_top_slice_pred.csv')
    df0 = pd.DataFrame()
    IDs = []
    errors = []
    count = 0
    for ID, c3_slice in zip(df['patient_id'], df['C3_Predict_slice']):
        count += 1
        try:
            CSA, sfat_area, vfat_area = get_c3_slice_area(
                patient_id=str(ID),
                c3_slice=c3_slice,
                seg_dir=seg_dir)
            CSD, sfat_density, vfat_density = get_c3_slice_density(
                patient_id=str(ID),
                c3_slice=c3_slice,
                seg_dir=seg_dir,
                img_dir=img_dir)
            print(count, ID, round(CSA, 2))
            df1 = pd.DataFrame({
                'patient_id': ID,
                'muscle_auto_segmentation_area': round(CSA, 2),
                'muscle_auto_edensity': round(CSD, 2)
                }, index=[0])
            df0 = df0.append(df1)
            df0.to_csv(proj_dir + '/c3_segmentation/clinical/C3_CSA.csv')
        except Exception as e:
            print(ID, e)
            IDs.append(ID)
            errors.append(e)
    print('bad data:', IDs, errors)


def CSA_review():
    df = pd.read_csv(proj_dir + '/inference/clinical/C3_CSA.csv')
    df0 = pd.read_csv(proj_dir + '/visualize/patient_list.csv')
    df = df0.merge(df, on


if __name__ == '__main__':

    proj_dir = '/mnt/kannlab_rfa/Zezhong'

    get_CSA(proj_dir)
