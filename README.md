import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_air_quality.csv")
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['date'] = df['datetime'].dt.date
    df['month'] = df['datetime'].dt.month
    df['hour'] = df['datetime'].dt.hour
    return df

df = load_data()

st.title(" Dashboard Kualitas Udara")
st.markdown("Visualisasi interaktif untuk data kualitas udara berdasarkan parameter polutan dan waktu.")

# Sidebar filter
stations = df['station'].unique().tolist()
selected_station = st.sidebar.selectbox("Pilih Stasiun:", stations)

filtered_df = df[df['station'] == selected_station]

# Rata-rata bulanan
st.subheader(f"Rata-rata Bulanan PM2.5 - {selected_station}")
monthly_avg = filtered_df.groupby('month')[['PM2.5']].mean()
fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(monthly_avg.index, monthly_avg['PM2.5'], marker='o')
ax1.set_xlabel("Bulan")
ax1.set_ylabel("PM2.5")
ax1.set_title("Rata-rata Bulanan PM2.5")
ax1.grid(True)
st.pyplot(fig1)

# Rata-rata harian
st.subheader(f"Rata-rata Harian PM2.5 - {selected_station}")
daily_avg = filtered_df.set_index('datetime').resample('D')[['PM2.5']].mean()
fig2, ax2 = plt.subplots(figsize=(15, 4))
ax2.plot(daily_avg.index, daily_avg['PM2.5'], color='orange')
ax2.set_title("Tren Harian PM2.5")
ax2.set_xlabel("Tanggal")
ax2.set_ylabel("PM2.5")
st.pyplot(fig2)

# Korelasi antar variabel
st.subheader("Korelasi Antar Variabel")
numeric_df = filtered_df.select_dtypes(include='number')
corr = numeric_df.corr()
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax3)
st.pyplot(fig3)

# Rata-rata per jam
st.subheader(f"Rata-rata PM2.5 per Jam - {selected_station}")
hourly_avg = filtered_df.groupby('hour')[['PM2.5']].mean()
fig4, ax4 = plt.subplots(figsize=(10, 4))
ax4.plot(hourly_avg.index, hourly_avg['PM2.5'], marker='o', color='green')
ax4.set_title("Rata-rata PM2.5 per Jam")
ax4.set_xlabel("Jam")
ax4.set_ylabel("PM2.5")
st.pyplot(fig4)

st.markdown("---")
st.markdown(" *Data dari file cleaned_air_quality.csv | Dibuat oleh Aristo Bima*")
