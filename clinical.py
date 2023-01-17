import pandas as pd
import numpy as np


def clinical():
    """
    Get cervical CSA, Lumbar CSA and lumbar SMI
    Args:
        proj_dir -- proj dir
    Returns:
        dataframe, csv
    """
    # ---get C3 segmention data---
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None
    proj_dir = '/mnt/kannlab_rfa/Zezhong/c3_segmentation'
    #area_NonOPC = pd.read_csv(proj_dir + '/inference/files/NonOPC_C3_body_comp_area_density.csv')
    #slice_NonOPC = pd.read_csv(proj_dir + '/inference/files/NonOPC_C3_top_slice_pred.csv')
    #area_OPC = pd.read_csv(proj_dir + '/inference/files/OPC_C3_body_comp_area_density.csv')
    #slice_OPC = pd.read_csv(proj_dir + '/inference/files/OPC_C3_top_slice_pred.csv')
    #NonOPC = area_NonOPC.merge(slice_NonOPC, on='patient_id', how='left').reset_index()
    #print('non opc:', NonOPC)
    #OPC = area_OPC.merge(slice_OPC, on='patient_id', how='left').reset_index()
    #print('opc:', OPC)
    #df0 = pd.concat([NonOPC, OPC], ignore_index=True)
    df_csa = pd.read_csv(proj_dir + '/clinical/C3_CSA.csv')
    df_slice = pd.read_csv(proj_dir + '/inference/files/C3_top_slice_pred.csv')
    df0 = df_csa.merge(df_slice, on='patient_id', how='left').reset_index()
    df0 = df0[['patient_id', 'muscle_auto_segmentation_area', 'muscle_auto_edensity', 
               'C3_Predict_slice', 'Z_spacing', 'XY_spacing']]
    df0.columns = ['PMRN', 'muscle_area', 'muscle_density', 'C3_slice', 'z_spacing', 'xy_spacing']
    df0['PMRN'] = df0['PMRN'].astype(float)
    #print('df:', df)

    # ---get clinical information---
    #meta = pd.read_csv(proj_dir + '/clinical/meta.csv', encoding='unicode_escape', low_memory=False)    
    df = pd.read_csv(proj_dir + '/clinical/meta.csv', encoding='unicode_escape')  
    # exclude surgery and induction cases
    df = df[~df['Pre-RT Neck Dissection'].isin(['Yes'])]
    df = df[~df['Pre-RT Primary Resection'].isin(['Yes'])]
    df = df[~df['Pre-RT Surgery'].isin(['Yes'])]
    df = df[~df['Radiation adjuvant to surgery'].isin(['Yes'])]
    #df = df[~df['Induction Chemotherapy'].isin(['Yes'])]

    #df['Weight'] = df['Pre-treatment Weight in Kilograms'].to_list()
    df['Weight'] = df['Pre-treatment Weight in Pounds'].values * 0.454
    df['BMI'] = df['Pre-treatment BMI'].to_list()
    df = df[df['Weight'].notna()]
    df = df[df['BMI'].notna()]
    df['Height'] = np.sqrt(df['Weight'] / df['BMI'])
    print('case number:', df.shape[0])
    ages = []
    for x, y in zip(df['Radiation Therapy Start Date'], df['Date of Birth']):
        #if np.isnan(x):
        if pd.isnull(x) or pd.isnull(y):
            age = 0
        else:
            x = int(str(x).split('/')[-1])
            y = int(str(y).split('/')[-1])
            if x > 80:
                # this would be 1980s or 1990s
                age = x - y
            else:
                # this would be 2000s, 2010s or 2020s
                age = x - y + 100
        ages.append(age)
    df['Age'] = ages
    df = df[df['Age'].notna()]
    df = df.merge(df0, on='PMRN', how='left').reset_index()
    df['CSA'] = df['muscle_area'].to_list()
    df['CSD'] = df['muscle_density'].to_list()
    df = df[df['CSA'].notna()]
    print('case number:', df.shape[0])
    df.to_csv(proj_dir + '/clinical/C3_test.csv', index=False)

    # ---get lumbar3 CSA and L3 SMI---
    L3_SMIs = []
    L3_CSAs = []
    bad_data = []
    errors = []
    for i in range(df.shape[0]):
        ID = df['PMRN'].iloc[i]
        gender = df['Gender'].iloc[i]
        CSA = df['CSA'].values[i]
        age = df['Age'].values[i]
        weight = df['Weight'].values[i]
        height = df['Height'].values[i]
        if gender == 'Female':
            sex = 1
        elif gender == 'Male':
            sex = 2
        else:
            print('input wrong gender info!')
        # CSA (cm2), age (years), weight (kg)
        L3_CSA = 27.304 + CSA*1.363 - age*0.671 + weight*0.640 + sex*26.422
        L3_SMI = L3_CSA/(height**2)
        L3_CSAs.append(L3_CSA)
        L3_SMIs.append(L3_SMI)
    df['L3_CSA'] = L3_CSAs
    df['L3_SMI'] = L3_SMIs
    df.to_csv(proj_dir + '/clinical/HN_C3_TOT.csv', index=False)


if __name__ == '__main__':

    clinical()





