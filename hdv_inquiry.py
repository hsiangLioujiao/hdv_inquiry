# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:32:07 2024

@author: g_s_s
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import seaborn as sns

#指定中文字型、字體大小
fm.fontManager.addfont('TaipeiSansTCBeta-Regular.ttf')
plt.rcParams["font.size"] = 14
plt.rcParams['font.family'] = 'Taipei Sans TC Beta'


# 讀取資料檔案
df = pd.read_csv("japan_2023.csv")


# 使用者輸入
st.header("日本重車能效資料")
vehicleType = st.selectbox("輸入車輛種類", ("大貨車", "大客車"))
brand = st.selectbox("輸入廠牌", ("FUSO", "HINO", "ISUZU"))
kind_x = st.radio(
    "選擇能效圖的x軸：",
    ["總重[噸]", "模擬車重[噸]"],
)


# 繪圖
fig = sns.relplot(data=df[(df["廠牌"]== brand) & (df["車輛種類"]== vehicleType)], x=kind_x, y="能效[km/L]", hue="排氣量[L]", style="排氣量[L]")
plt.title(f"日本2023年度{brand}{vehicleType}新車能效")
plt.ylabel("能效[km/L]")
plt.xlabel(kind_x)
plt.xlim([0,60])
plt.ylim([0,15])
plt.show()


# streamlit繪圖
st.pyplot(fig)

st.divider()


# 查詢總重範圍車款
st.subheader(f"依總重查詢日本2023年度{brand}{vehicleType}新車資料：")
with st.form("my_form"):
    col1, col2 = st.columns(2)
    gvw_d = col1.number_input("總重下限(不含)", value=3.5)
    gvw_u = col2.number_input("總重上限(含)", value=60)
    
    submitted = st.form_submit_button("送出")
    if submitted:
        df_s = df[(df["廠牌"]==brand) & (df["車輛種類"]==vehicleType) & (df["總重[噸]"]>gvw_d) & (df["總重[噸]"]<=gvw_u)]
        st.dataframe(df_s)
        st.write(f"有{len(df_s)}款車，平均能效{df_s['能效[km/L]'].mean():.2f} km/L")

st.divider()

st.write("資料來源:日本國土交通省 新車能效認證資料。")
st.write("https://www.mlit.go.jp/jidosha/jidosha_fr10_000056.html")
