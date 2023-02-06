import os
import pandas as pd
import SimpleITK as sitk
import numpy as np
from src.slice_area_density import get_c3_slice_area, get_c3_slice_density


def get_CSA():
    """get C3 muscle area and density
    """
    proj_dir = '/mnt/kannlab_rfa/Zezhong/c3_segmentation'
    #img_dir = proj_dir + '/internal_test/prepro_img'
    #seg_dir = proj_dir + '/internal_test/prepro_seg'
    #pred_dir = proj_dir + '/internal_test/segmentation_model/preds'
    #pred_dir = proj_dir + '/internal_test/pred_seg'
    img_dir = proj_dir + '/internal_test/yash_img'
    seg_dir = proj_dir + '/internal_test/yash_seg'
    #pred_dir = proj_dir + '/internal_test/segmentation_model/preds'
    pred_dir = proj_dir + '/internal_test/yash_pred'
    csv_path = proj_dir + '/internal_test/clinical_data/sum.csv'
    df = pd.read_csv(csv_path)
    pred_csas = []
    pred_csds = []
    seg_csas = []
    seg_csds = []
    pred_voxels = []
    seg_voxels = []
    count = 0
    for ID, pred_slice, seg_slice in zip(df['ID'], df['pred_slice'], df['seg_slice']):
        count += 1
        ID = str(ID)
        # prediction CSA
        csa, csd, tot_voxel = get_c3_slice_area(
            patient_id=ID,
            c3_slice=pred_slice,
            img_dir=img_dir,
            seg_dir=pred_dir)
        pred_csa = round(csa, 2)
        pred_csd = round(csd, 2)
        pred_voxel = tot_voxel
        pred_csas.append(pred_csa)
        pred_csds.append(pred_csd)
        pred_voxels.append(pred_voxel)
        # segmentation CSA
        csa, csd, tot_voxel = get_c3_slice_area(
            patient_id=ID,
            c3_slice=seg_slice,
            img_dir=img_dir,
            seg_dir=seg_dir)
        seg_csa = round(csa, 2)
        seg_csd = round(csd, 2)
        seg_voxel = tot_voxel
        seg_csas.append(seg_csa)
        seg_csds.append(seg_csd)
        seg_voxels.append(seg_voxel)
        #print(count, ID, seg_csa, pred_csa, seg_csd, pred_csd)
        print(count, ID, seg_csa, seg_voxel, pred_csa, pred_voxel)
    #df['seg_csa'], df['pred_csa'], df['seg_csd'], df['pred_csd'] = [seg_csas, pred_csas, seg_csds, pred_csds]
    df['seg_csa'], df['pred_csa'], df['seg_voxel'], df['pred_voxel'] = [seg_csas, pred_csas, seg_voxels, pred_voxels]
    save_path = proj_dir + '/internal_test/clinical_data/sum_yash.csv'
    df.to_csv(save_path, index=False)


if __name__ == '__main__':

    proj_dir = '/mnt/kannlab_rfa/Zezhong'

    get_CSA(proj_dir)
