pip install seaborn
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

# Fitur interaktif: Pilih satu atau lebih musim
selected_seasons = st.multiselect("Pilih Musim untuk Ditampilkan:", 
                                  options=season_trend['season'].unique(),
                                  default=season_trend['season'].unique()) # Default pilih semua musim

# Filter data berdasarkan pilihan musim
filtered_data = season_trend[season_trend['season'].isin(selected_seasons)]

# Tampilkan data
st.subheader(f"Data Penyewaan Sepeda untuk Musim {', '.join(selected_seasons)}")
st.dataframe(filtered_data)

# Plot 1: Bar Chart Perubahan Casual & Registered
st.subheader(f"Perubahan Penyewaan Casual & Registered di Musim {', '.join(selected_seasons)}")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=filtered_data, x='season', y='casual_diff', color='blue', label='Casual Diff', ax=ax)
sns.barplot(data=filtered_data, x='season', y='registered_diff', color='red', label='Registered Diff', ax=ax)
ax.axhline(0, color='black', linestyle='--')
ax.set_ylabel("Perubahan Jumlah Penyewa")
ax.set_xlabel("Musim")
ax.legend()
st.pyplot(fig)

# Plot 2: Line Chart Tren Penyewaan Casual & Registered
st.subheader(f"Tren Penyewaan Sepeda Casual & Registered di Musim {', '.join(selected_seasons)}")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=filtered_data, x='season', y='casual', marker='o', label='Casual', color='blue', ax=ax)
sns.lineplot(data=filtered_data, x='season', y='registered', marker='o', label='Registered', color='red', ax=ax)
ax.set_ylabel("Total Penyewa")
ax.set_xlabel("Musim")
ax.legend()
st.pyplot(fig)

# Plot 3: Pie Chart Proporsi Penyewaan
st.subheader(f"Proporsi Penyewaan Sepeda di Musim {', '.join(selected_seasons)}")
fig, ax = plt.subplots()
ax.pie(filtered_data[['casual', 'registered']].sum(), 
       labels=['Casual', 'Registered'], 
       autopct='%1.1f%%', 
       colors=['blue', 'red'])
st.pyplot(fig)

# Kesimpulan berdasarkan filter musim
st.subheader(f"Kesimpulan Tren Penyewaan di Musim {', '.join(selected_seasons)}")
st.write(filtered_data[['season', 'trend']])

# Tambahkan insight tambahan
st.markdown("""
### 📌 Insight:
1. Penyewaan sepeda di musim **Fall** cenderung lebih tinggi dibanding musim lainnya.
2. Penyewa **casual lebih fluktuatif**, sementara penyewa **registered lebih stabil**.
3. **Musim dingin** (Winter) memiliki penyewaan yang lebih rendah, kemungkinan karena kondisi cuaca yang kurang mendukung.
4. **Peningkatan strategi pemasaran** bisa difokuskan pada musim dengan penyewaan rendah seperti Spring dan Winter.
""")
