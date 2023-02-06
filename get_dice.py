import numpy as np
import os
import pandas as pd
import glob
import SimpleITK as sitk
from src.slice_area_density import get_c3_slice_area


def get_dice():
    proj_dir = '/mnt/kannlab_rfa/Zezhong/c3_segmentation'
    #img_dir = proj_dir + '/internal_test/prepro_img'
    #seg_dir = proj_dir + '/internal_test/prepro_seg'
    #pred_dir = proj_dir + '/internal_test/pred_seg'
    img_dir = proj_dir + '/internal_test/yash_img'
    seg_dir = proj_dir + '/internal_test/yash_seg'
    pred_dir = proj_dir + '/internal_test/yash_pred'
    slice_csv_path = proj_dir + '/internal_test/slice_model/slice_tot.csv'
    inters = []
    sums = []
    unions = []
    dices = []
    df = pd.read_csv(slice_csv_path)
    for ID, pred_slice, seg_slice in zip(df['ID'], df['pred_slice'], df['seg_slice']):
        pred_path = pred_dir + '/' + ID + '.nrrd'
        seg_path = seg_dir + '/' + ID + '.nrrd'
        pred = sitk.ReadImage(pred_path)
        pred = sitk.GetArrayFromImage(pred)
        pred = pred[pred_slice, :, :]
        seg = sitk.ReadImage(seg_path)
        seg = sitk.GetArrayFromImage(seg)
        seg = seg[seg_slice, :, :]
        #pred = np.where(pred != 0.0, 1, 0)
        #seg = np.where(seg != 0.0, 1, 0)
        dice = (2*np.sum(seg*pred)) / (np.sum(seg) + np.sum(pred))
        print(round(dice, 3))
        #pred = np.where(pred != 0.0, 1, 0)
        #seg = np.where(seg != 0.0, 1, 0)
        assert pred.shape == seg.shape, print('different shape')
        pred = pred.astype(bool)
        seg = seg.astype(bool)
        volume_sum = seg.sum() + pred.sum()
        volume_intersect = (seg & pred).sum()
        volume_union = volume_sum - volume_intersect
        #dice = 2*volume_intersect / volume_sum
        #dice = round(dice, 3)
        #print(ID, dice)
        inters.append(volume_intersect)
        sums.append(volume_sum)
        unions.append(volume_union)
        dices.append(dice)
    print('dice:', dices)
    print('median dice:', np.nanmedian(dices))
    print('mean dice:', round(np.nanmean(dices), 3))
    dsc_agg = round(2*sum(inters)/sum(sums), 3)
    jaccard_agg = round(sum(inters)/sum(unions), 3)
    print('aggregated dice score:', dsc_agg)
    print('aggregated jaccard score:', jaccard_agg)
    df['dice'] = dices
    df.to_csv(proj_dir + '/internal_test/slice_model/slice_yash.csv')


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

    get_dice()
    #get_CSA()



