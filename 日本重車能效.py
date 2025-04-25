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

#指定中文字型、字體大小
fm.fontManager.addfont('TaipeiSansTCBeta-Regular.ttf')
plt.rcParams["font.size"] = 14
plt.rcParams['font.family'] = 'Taipei Sans TC Beta'

st.set_page_config(
    page_title="功能打樣版 僅供3人同時使用",
    page_icon="random",
)




# 讀取資料檔案
df = pd.read_csv("japan_2025.csv")


# 使用者輸入
st.header("日本重車能效資料")
vehicleType = st.selectbox("輸入車輛種類", list(df["車輛種類"].unique()))
brand = st.selectbox("輸入廠牌", list(df[df["車輛種類"]==vehicleType]["廠牌"].unique()))
kind_x = st.radio(
    "選擇能效圖的x軸：",
    ["總重[噸]", "模擬車重[噸]"],
)


# 繪圖
hue_order = sorted(list(df[(df["廠牌"]== brand) & (df["車輛種類"]== vehicleType)]["總排氣量[L]"].unique()))
hue_order = [str(i) for i in hue_order]
df.loc[:,'總排氣量[L]'] = df['總排氣量[L]'].astype('str')
fig = sns.relplot(data=df[(df["廠牌"]== brand) & (df["車輛種類"]== vehicleType)], x=kind_x, y="能效[km/L]", hue="總排氣量[L]", style="總排氣量[L]", hue_order=hue_order)
plt.title(f"日本2025年{brand}{vehicleType}新車能效")
plt.ylabel("能效[km/L]")
plt.xlabel(kind_x)
plt.xlim([0,60])
plt.ylim([0,15])
plt.show()
df.loc[:,'總排氣量[L]'] = df['總排氣量[L]'].astype('float')


# streamlit繪圖
st.pyplot(fig)

st.divider()


# 查詢總重範圍車款
st.subheader(f"依總重查詢日本2025年{brand}{vehicleType}新車資料：")
with st.form("my_form"):
    col1, col2 = st.columns(2)
    gvw_d = col1.number_input("總重下限(不含)", value=math.floor(df[(df["廠牌"]== brand) & (df["車輛種類"]== vehicleType)]["總重[噸]"].min()))
    gvw_u = col2.number_input("總重上限(含)", value=math.ceil(df[(df["廠牌"]== brand) & (df["車輛種類"]== vehicleType)]["總重[噸]"].max()))
    
    if st.form_submit_button("送出"):
        df_s = df[(df["廠牌"]==brand) & (df["車輛種類"]==vehicleType) & (df["總重[噸]"]>gvw_d) & (df["總重[噸]"]<=gvw_u)].drop(columns=['車輛種類', '廠牌'])
        st.dataframe(df_s)
        st.write(f"有{len(df_s)}款車，能效{df_s['能效[km/L]'].min():.2f}~{df_s['能效[km/L]'].max():.2f} km/L，平均能效{df_s['能效[km/L]'].mean():.2f} km/L。")


st.divider()

st.write("資料來源:日本國土交通省 新車能效認證資料。")
st.write("https://www.mlit.go.jp/jidosha/jidosha_fr10_000056.html")
