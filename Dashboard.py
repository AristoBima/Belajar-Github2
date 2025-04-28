# dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import datetime


# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Kualitas Udara", layout="wide")

# ================================
# BAGIAN 1: Data Gathering (PRSA Data)
# ================================

st.title("Dashboard - Gathering Data (PRSA Dataset)")

# Load data
@st.cache_data
def load_prsa_data():
    df_prsa = pd.read_csv("PRSA_Data_Aotizhongxin_20130301-20170228.csv")
    df_prsa['date'] = pd.to_datetime(df_prsa['year'].astype(str) + '-' + df_prsa['month'].astype(str) + '-' + df_prsa['day'].astype(str) + ' ' + df_prsa['hour'].astype(str) + ':00')
    return df_prsa

df_prsa = load_prsa_data()

# Range waktu
min_date = df_prsa['date'].min()
max_date = df_prsa['date'].max()

selected_date = st.slider(
    "Pilih rentang waktu untuk PRSA Data:",
    min_value=min_date.to_pydatetime(),
    max_value=max_date.to_pydatetime(),
    value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
    format="YYYY-MM-DD"
)
# Filter berdasarkan tanggal
filtered_prsa = df_prsa[(df_prsa['date'] >= selected_date[0]) & (df_prsa['date'] <= selected_date[1])]

st.dataframe(filtered_prsa)

# Visualisasi Suhu (TEMP) terhadap Waktu
st.line_chart(filtered_prsa.set_index('date')['TEMP'])

st.markdown("---")

# ================================
# BAGIAN 2: Dashboard Kualitas Udara (Cleaned Data)
# ================================

st.title("Dashboard Kualitas Udara - Cleaned Dataset")

st.markdown("Visualisasi interaktif untuk data kualitas udara berdasarkan parameter polutan dan waktu.")

# Load cleaned data
@st.cache_data
def load_cleaned_data():
    df_cleaned = pd.read_csv("cleaned_air_quality.csv")
    df_cleaned['datetime'] = pd.to_datetime(df_cleaned['datetime'])
    df_cleaned['date'] = df_cleaned['datetime'].dt.date
    df_cleaned['month'] = df_cleaned['datetime'].dt.month
    df_cleaned['hour'] = df_cleaned['datetime'].dt.hour
    return df_cleaned

df_cleaned = load_cleaned_data()

# Sidebar filter stasiun
stations = df_cleaned['station'].unique().tolist()
selected_station = st.sidebar.selectbox("Pilih Stasiun:", stations)

filtered_cleaned = df_cleaned[df_cleaned['station'] == selected_station]

# Visualisasi rata-rata bulanan PM2.5
st.subheader(f"Rata-rata Bulanan PM2.5 - {selected_station}")
monthly_avg = filtered_cleaned.groupby('month')[['PM2.5']].mean()

fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(monthly_avg.index, monthly_avg['PM2.5'], marker='o')
ax1.set_xlabel("Bulan")
ax1.set_ylabel("PM2.5")
ax1.set_title("Rata-rata Bulanan PM2.5")
ax1.grid(True)
st.pyplot(fig1)

# Visualisasi tren harian PM2.5
st.subheader(f"Rata-rata Harian PM2.5 - {selected_station}")
daily_avg = filtered_cleaned.set_index('datetime').resample('D')[['PM2.5']].mean()

fig2, ax2 = plt.subplots(figsize=(15, 4))
ax2.plot(daily_avg.index, daily_avg['PM2.5'], color='orange')
ax2.set_xlabel("Tanggal")
ax2.set_ylabel("PM2.5")
ax2.set_title("Tren Harian PM2.5")
st.pyplot(fig2)

# Korelasi antar variabel
st.subheader("Korelasi Antar Variabel")
numeric_df = filtered_cleaned.select_dtypes(include='number')
corr = numeric_df.corr()

fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax3)
st.pyplot(fig3)

# Visualisasi rata-rata PM2.5 per jam
st.subheader(f"Rata-rata PM2.5 per Jam - {selected_station}")
hourly_avg = filtered_cleaned.groupby('hour')[['PM2.5']].mean()

fig4, ax4 = plt.subplots(figsize=(10, 4))
ax4.plot(hourly_avg.index, hourly_avg['PM2.5'], marker='o', color='green')
ax4.set_xlabel("Jam")
ax4.set_ylabel("PM2.5")
ax4.set_title("Rata-rata PM2.5 per Jam")
st.pyplot(fig4)

st.markdown("---")
st.markdown("*Data dari file cleaned_air_quality.csv | Dibuat oleh Aristo Bima*")

