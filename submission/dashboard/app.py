import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df_day = pd.read_csv("day.csv")

# Mapping season
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df_day['season'] = df_day['season'].map(season_mapping)

# Group by season
season_trend = df_day.groupby('season')[['casual', 'registered', 'cnt']].sum().reset_index()

# Hitung perubahan dari musim ke musim
season_trend['casual_diff'] = season_trend['casual'].diff().fillna(0)
season_trend['registered_diff'] = season_trend['registered'].diff().fillna(0)

# Tambahkan kategori tren
season_trend['trend'] = season_trend.apply(
    lambda row: 'Casual ↓, Registered ↑' if row['casual_diff'] < 0 and row['registered_diff'] > 0 else
                'Casual ↑, Registered ↓' if row['casual_diff'] > 0 and row['registered_diff'] < 0 else 
                'Sama-sama Naik' if row['casual_diff'] > 0 and row['registered_diff'] > 0 else 
                'Sama-sama Turun', axis=1)

# Streamlit UI
st.title("Dashboard Analisis Penyewaan Sepeda 🚴")

# Tampilkan data
st.subheader("Data Penyewaan Sepeda per Musim")
st.dataframe(season_trend)

# Plot 1: Bar Chart Perubahan Casual & Registered
st.subheader("Perubahan Penyewaan Casual & Registered per Musim")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=season_trend, x='season', y='casual_diff', color='blue', label='Casual Diff', ax=ax)
sns.barplot(data=season_trend, x='season', y='registered_diff', color='red', label='Registered Diff', ax=ax)
ax.axhline(0, color='black', linestyle='--')
ax.set_ylabel("Perubahan Jumlah Penyewa")
ax.set_xlabel("Musim")
ax.legend()
st.pyplot(fig)

# Plot 2: Line Chart Tren Penyewaan Casual & Registered
st.subheader("Tren Penyewaan Sepeda Casual & Registered per Musim")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=season_trend, x='season', y='casual', marker='o', label='Casual', color='blue', ax=ax)
sns.lineplot(data=season_trend, x='season', y='registered', marker='o', label='Registered', color='red', ax=ax)
ax.set_ylabel("Total Penyewa")
ax.set_xlabel("Musim")
ax.legend()
st.pyplot(fig)

st.subheader("Kesimpulan Tren Penyewaan")
st.write(season_trend[['season', 'trend']])
