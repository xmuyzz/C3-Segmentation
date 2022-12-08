import pandas as pd
import numpy as np


def clinical():
    
    # get C3 segmention data
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None
    proj_dir = '/mnt/kannlab_rfa/Zezhong/c3_segmentation'
    area_NonOPC = pd.read_csv(proj_dir + '/output/NonOPC_C3_body_comp_area_density.csv')
    slice_NonOPC = pd.read_csv(proj_dir + '/output/NonOPC_C3_top_slice_pred.csv')
    area_OPC = pd.read_csv(proj_dir + '/output/OPC_C3_body_comp_area_density.csv')
    slice_OPC = pd.read_csv(proj_dir + '/output/OPC_C3_top_slice_pred.csv')
    NonOPC = area_NonOPC.merge(slice_NonOPC, on='patient_id', how='left').reset_index()
    #print('non opc:', NonOPC)
    OPC = area_OPC.merge(slice_OPC, on='patient_id', how='left').reset_index()
    #print('opc:', OPC)
    df = pd.concat([NonOPC, OPC], ignore_index=True)
    df = df[['patient_id', 'muscle_auto_segmentation_area', 'muscle_auto_edensity', 
             'C3_Predict_slice', 'Z_spacing', 'XY_spacing']]
    df.columns = ['PMRN', 'muscle_area', 'muscle_density', 'C3_slice', 'z_spacing', 'xy_spacing']
    df['PMRN'] = df['PMRN'].astype(float)
    #print('df:', df)

    # get clinical information
    meta = pd.read_csv(proj_dir + '/clinical/meta.csv', encoding='unicode_escape', low_memory=False)
    
    df = df.merge(meta, on='PMRN', how='left').reset_index()
    #print(df)
    #df.to_csv(proj_dir + '/clinical/C3_all.csv', index=False)
    
    # get heights
    df['height'] = np.sqrt(df['Pre-treatment Weight in Kilograms'] / df['Pre-treatment BMI'])
    print(df['height'])
    ages = []
    for x, y in zip(df['Radiation Therapy Start Date'], df['Date of Birth']):
        #if np.isnan(x):
        if pd.isnull(x) or pd.isnull(y):
            age = 0
        else:
            x = int(str(x).split('/')[-1])
            y = int(str(y).split('/')[-1])
            age = x - y + 100
            ages.append(age)
    df['age'] = ages
    df['density/height'] = df['muscle_density'] / df['height']
    df['density/age'] = df['muscle_density'] / df['age']
    df['area/height'] = df['muscle_area'] / df['height']
    df['area/age'] = df['muscle_area'] / df['age']
    df.to_csv(proj_dir + '/clinical/C3_all.csv', index=False)




if __name__ == '__main__':

    clinical()
