import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Membaca data
day_data = pd.read_csv('day.csv')

# --- Sidebar dan Widget ---
st.sidebar.title("Opsi Pengaturan")

# Slider untuk memilih rentang hari
min_date = day_data['dteday'].min()
max_date = day_data['dteday'].max()
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [pd.to_datetime(min_date), pd.to_datetime(max_date)])

# Selectbox untuk memilih musim atau perbandingan seluruh musim
season_labels = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
season_options = ['Semua Musim'] + list(season_labels.values())
season_selection = st.sidebar.selectbox("Pilih Musim atau Bandingkan Semua Musim", season_options)

# Checkbox untuk menampilkan atau menyembunyikan outliers
show_outliers = st.sidebar.checkbox("Tampilkan Outliers", value=True)

# Radio button untuk memilih tipe visualisasi
visualization_type = st.sidebar.radio(
    "Pilih Tipe Visualisasi", 
    ('Distribusi Musim', 'Pengaruh Cuaca', 'Hari Kerja vs Akhir Pekan')
)

# --- Visualisasi dan Interaktivitas ---
st.title("Analisis Penyewaan Sepeda Harian")

# Tampilkan rentang tanggal yang dipilih
st.subheader(f"Data dari {date_range[0]} hingga {date_range[1]}")
filtered_data = day_data[(pd.to_datetime(day_data['dteday']) >= pd.to_datetime(date_range[0])) & 
                         (pd.to_datetime(day_data['dteday']) <= pd.to_datetime(date_range[1]))]

# Visualisasi Distribusi Musim atau Perbandingan Semua Musim
if visualization_type == 'Distribusi Musim':
    if season_selection == 'Semua Musim':
        st.subheader("Perbandingan Jumlah Penyewaan Sepeda Berdasarkan Semua Musim")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(x='season', y='cnt', data=filtered_data if show_outliers else filtered_data[filtered_data['cnt'] < filtered_data['cnt'].quantile(0.95)], ax=ax)
        ax.set_title('Distribusi Jumlah Penyewaan Sepeda Berdasarkan Semua Musim')
        ax.set_xlabel('Musim')
        ax.set_ylabel('Jumlah Penyewaan Sepeda (cnt)')
        ax.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'])
        st.pyplot(fig)
    
    else:
        st.subheader(f"Distribusi Jumlah Penyewaan Sepeda Berdasarkan Musim: {season_selection}")
        season_key = [key for key, value in season_labels.items() if value == season_selection][0]
        season_filtered_data = filtered_data[filtered_data['season'] == season_key]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(x='season', y='cnt', data=season_filtered_data if show_outliers else season_filtered_data[season_filtered_data['cnt'] < season_filtered_data['cnt'].quantile(0.95)], ax=ax)
        ax.set_title(f'Distribusi Jumlah Penyewaan Sepeda (Musim: {season_selection})')
        ax.set_xlabel('Musim')
        ax.set_ylabel('Jumlah Penyewaan Sepeda (cnt)')
        ax.set_xticklabels([season_selection])
        st.pyplot(fig)

# Visualisasi Pengaruh Cuaca
elif visualization_type == 'Pengaruh Cuaca':
    if season_selection == 'Semua Musim':
        st.subheader("Korelasi Cuaca dengan Penyewaan Sepeda Berdasarkan Semua Musim")
    else:
        st.subheader(f"Korelasi Cuaca dengan Penyewaan Sepeda pada Musim: {season_selection}")
        season_key = [key for key, value in season_labels.items() if value == season_selection][0]
        filtered_data = filtered_data[filtered_data['season'] == season_key]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Plot Pengaruh Suhu
    sns.scatterplot(x='temp', y='cnt', data=filtered_data, ax=axes[0])
    axes[0].set_title('Pengaruh Suhu terhadap Jumlah Penyewaan Sepeda')
    axes[0].set_xlabel('Suhu (Ternormalisasi)')
    axes[0].set_ylabel('Jumlah Penyewaan Sepeda')

    # Plot Pengaruh Kelembaban
    sns.scatterplot(x='hum', y='cnt', data=filtered_data, ax=axes[1])
    axes[1].set_title('Pengaruh Kelembaban terhadap Jumlah Penyewaan Sepeda')
    axes[1].set_xlabel('Kelembaban (Ternormalisasi)')

    # Plot Pengaruh Kecepatan Angin
    sns.scatterplot(x='windspeed', y='cnt', data=filtered_data, ax=axes[2])
    axes[2].set_title('Pengaruh Kecepatan Angin terhadap Jumlah Penyewaan Sepeda')
    axes[2].set_xlabel('Kecepatan Angin (Ternormalisasi)')

    plt.tight_layout()
    st.pyplot(fig)

# Visualisasi Hari Kerja vs Akhir Pekan
else:
    if season_selection == 'Semua Musim':
        st.subheader("Pengaruh Hari Kerja vs Akhir Pekan pada Semua Musim")
    else:
        st.subheader(f"Pengaruh Hari Kerja vs Akhir Pekan pada Musim: {season_selection}")
        season_key = [key for key, value in season_labels.items() if value == season_selection][0]
        filtered_data = filtered_data[filtered_data['season'] == season_key]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='workingday', y='cnt', data=filtered_data, ax=ax)
    ax.set_title('Pengaruh Hari Kerja dan Akhir Pekan Terhadap Jumlah Penyewaan Sepeda')
    ax.set_xlabel('Hari Kerja (1: Hari Kerja, 0: Hari Libur)')
    ax.set_ylabel('Jumlah Penyewaan Sepeda')
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Hari Libur', 'Hari Kerja'])
    st.pyplot(fig)

# Widget tambahan: informasi rata-rata penyewaan sepeda
if st.sidebar.checkbox("Tampilkan Rata-rata Penyewaan Sepeda"):
    st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Rentang Tanggal dan Musim Terpilih")
    avg_rentals = filtered_data['cnt'].mean()
    st.write(f"Rata-rata Penyewaan Sepeda: {avg_rentals:.2f}")
