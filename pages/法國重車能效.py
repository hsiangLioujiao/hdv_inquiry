# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:32:07 2024

@author: g_s_s
"""

import math
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import seaborn as sns


pd.options.mode.copy_on_write = True # 關於df.loc[:,'...'] = ...之設定

fm.fontManager.addfont('TaipeiSansTCBeta-Regular.ttf')
plt.rcParams["font.size"] = 14
plt.rcParams['font.family'] = 'Taipei Sans TC Beta'

st.set_page_config(
    page_title="功能打樣版 僅供3人同時使用",
    page_icon="random",
)




@st.cache_data
def my_read():
    df = pd.read_csv("DataExtract_FR.csv",
                     usecols=['OEM_Make', 'OEM_Model', 'OEM_VehicleGroup', 'OEM_GrossVehicleMass_t',
                              'Engine_RatedPower_kw', 'Engine_Displacement_ltr',
                              'RDL_TotalVehicleMass_kg', 'RDL_FuelConsumption_l100km',
                              'RDR_TotalVehicleMass_kg', 'RDR_FuelConsumption_l100km',
                              'LHL_TotalVehicleMass_kg', 'LHL_FuelConsumption_l100km',
                              'LHR_TotalVehicleMass_kg', 'LHR_FuelConsumption_l100km'])
    df.dropna(axis=0, how='any', inplace=True)
    
    df.loc[:,'長途輕載能效[km/L]'] = 100./df['LHL_FuelConsumption_l100km']
    df.loc[:,'長途參考載重能效[km/L]'] = 100./df['LHR_FuelConsumption_l100km']
    df.loc[:,'城際輕載能效[km/L]'] = 100./df['RDL_FuelConsumption_l100km']
    df.loc[:,'城際參考載重能效[km/L]'] = 100./df['RDR_FuelConsumption_l100km']
    df.drop(columns=['LHL_FuelConsumption_l100km', 'LHR_FuelConsumption_l100km', 'RDL_FuelConsumption_l100km', 'RDR_FuelConsumption_l100km'], inplace=True)

    df.loc[:,'長途輕載模擬車重[噸]'] = df['LHL_TotalVehicleMass_kg']/1000.
    df.loc[:,'長途參考載重模擬車重[噸]'] = df['LHR_TotalVehicleMass_kg']/1000.
    df.loc[:,'城際輕載模擬車重[噸]'] = df['RDL_TotalVehicleMass_kg']/1000.
    df.loc[:,'城際參考載重模擬車重[噸]'] = df['RDR_TotalVehicleMass_kg']/1000.
    df.drop(columns=['LHL_TotalVehicleMass_kg', 'LHR_TotalVehicleMass_kg', 'RDL_TotalVehicleMass_kg', 'RDR_TotalVehicleMass_kg'], inplace=True)

    
    df_L = df[['OEM_Make', 'OEM_Model', 'OEM_VehicleGroup', 'OEM_GrossVehicleMass_t', 'Engine_RatedPower_kw', 'Engine_Displacement_ltr',
               '城際輕載模擬車重[噸]', '城際輕載能效[km/L]']]
    df_L.columns=['OEM_Make', 'OEM_Model', 'OEM_VehicleGroup', '總重[噸]', 'Engine_RatedPower_kw', '總排氣量[L]',
                  '模擬車重[噸]', '能效[km/L]']
    df_L['載重別'] = "歐盟輕載"
    df_L['行車型態別'] = "歐盟城際運輸"
    
    df_L_tmp = df[['OEM_Make', 'OEM_Model', 'OEM_VehicleGroup', 'OEM_GrossVehicleMass_t', 'Engine_RatedPower_kw', 'Engine_Displacement_ltr',
                   '城際參考載重模擬車重[噸]', '城際參考載重能效[km/L]']]
    df_L_tmp.columns=['OEM_Make', 'OEM_Model', 'OEM_VehicleGroup', '總重[噸]', 'Engine_RatedPower_kw', '總排氣量[L]',
                      '模擬車重[噸]', '能效[km/L]']
    df_L_tmp['載重別'] = "歐盟參考載重"
    df_L_tmp['行車型態別'] = "歐盟城際運輸"
    df_L = pd.concat([df_L, df_L_tmp], ignore_index=True)
    
    df_L_tmp = df[['OEM_Make', 'OEM_Model', 'OEM_VehicleGroup', 'OEM_GrossVehicleMass_t', 'Engine_RatedPower_kw', 'Engine_Displacement_ltr',
                   '長途輕載模擬車重[噸]', '長途輕載能效[km/L]']]
    df_L_tmp.columns=['OEM_Make', 'OEM_Model', 'OEM_VehicleGroup', '總重[噸]', 'Engine_RatedPower_kw', '總排氣量[L]',
                      '模擬車重[噸]', '能效[km/L]']
    df_L_tmp['載重別'] = "歐盟輕載"
    df_L_tmp['行車型態別'] = "歐盟長途運輸"
    df_L = pd.concat([df_L, df_L_tmp], ignore_index=True)
    
    df_L_tmp = df[['OEM_Make', 'OEM_Model', 'OEM_VehicleGroup', 'OEM_GrossVehicleMass_t', 'Engine_RatedPower_kw', 'Engine_Displacement_ltr',
                   '長途參考載重模擬車重[噸]', '長途參考載重能效[km/L]']]
    df_L_tmp.columns=['OEM_Make', 'OEM_Model', 'OEM_VehicleGroup', '總重[噸]', 'Engine_RatedPower_kw', '總排氣量[L]',
                      '模擬車重[噸]', '能效[km/L]']
    df_L_tmp['載重別'] = "歐盟參考載重"
    df_L_tmp['行車型態別'] = "歐盟長途運輸"
    df_L = pd.concat([df_L, df_L_tmp], ignore_index=True)

    return(df_L)
    



df = my_read()

vehicleTypeGroup = {"大貨車": [1, 2, 3, 4, 5, 9, 11], "全聯結車(曳引車)": [10, 12]}
st.header("法國重車能效資料")
vehicleType = st.selectbox("輸入車輛種類", ["大貨車", "全聯結車(曳引車)"])
brand = st.selectbox("輸入廠牌", list(df[df['OEM_VehicleGroup'].isin(vehicleTypeGroup[vehicleType])]['OEM_Make'].unique()))
kind_pattern = st.radio("選擇行車型態：", list(df[df['OEM_VehicleGroup'].isin(vehicleTypeGroup[vehicleType]) &
                                               (df['OEM_Make']==brand)]['行車型態別'].unique()))
df_U = df[(df['OEM_VehicleGroup'].isin(vehicleTypeGroup[vehicleType])) & (df['OEM_Make']==brand) & (df['行車型態別']==kind_pattern)]

kind_x = st.radio(
    "選擇能效圖的x軸：",
    ["總重[噸]", "模擬車重[噸]"],
)


hue_order = sorted(list(df_U['總排氣量[L]'].unique()))
hue_order = [str(i) for i in hue_order]
df_U.loc[:,'Engine_Displacement_ltr'] = df_U['總排氣量[L]'].astype('str')
fig = sns.relplot(data=df_U, x=kind_x, y="能效[km/L]", hue="總排氣量[L]", style="總排氣量[L]", hue_order=hue_order)
plt.title(f"法國{brand}{vehicleType}新車{kind_pattern[2:]}能效")
plt.ylabel("能效[km/L]")
plt.xlabel(kind_x)
# plt.xlim([0,60])
# plt.ylim([0,15])
plt.show()
df_U.loc[:,'總排氣量[L]'] = df_U['總排氣量[L]'].astype('float')
print(df_U['OEM_VehicleGroup'].unique())
print(df_U['OEM_Make'].unique())
print(df_U['行車型態別'].unique())
print()

# streamlit繪圖
st.pyplot(fig)

st.divider()


# 查詢總重範圍車款
st.subheader(f"依總重查詢法國{brand}{vehicleType}新車{kind_pattern[2:]}資料：")
with st.form("my_form"):
    col1, col2 = st.columns(2)
    gvw_d = col1.number_input("總重下限(不含)", value=math.floor(df_U["總重[噸]"].min()))
    gvw_u = col2.number_input("總重上限(含)", value=math.ceil(df_U["總重[噸]"].max()))
    
    if st.form_submit_button("送出"):
        df_s = df_U[(df_U["總重[噸]"]>gvw_d) & (df_U["總重[噸]"]<=gvw_u)].drop(columns=['OEM_Make', 'OEM_VehicleGroup'])
        st.dataframe(df_s)
        st.write(f"有{len(df_s)}款車，能效{df_s['能效[km/L]'].min():.2f}~{df_s['能效[km/L]'].max():.2f} km/L，平均能效{df_s['能效[km/L]'].mean():.2f} km/L。")


st.divider()

st.write("資料來源:歐盟環境部 新車能效認證資料。")
st.write("https://www.eea.europa.eu/en/datahub/datahubitem-view/c52f7b51-c1cf-43e5-9a66-3eea19f6385a")
