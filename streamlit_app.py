import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("Bike Sharing Analysis Dashboard")
st.write(
    "Berikut adalah hasil analisis data sepeda yang dirental sepanjang tahun 2011 sampai 2012."
)

# Membaca data CSV
day_df = pd.read_csv("data/day.csv")
hour_df = pd.read_csv("data/hour.csv")

# Menampilkan data harian
st.write("## Data Harian")
day_data = day_df.copy()

# Pastikan kolom tanggal adalah tipe datetime
day_data["dteday"] = pd.to_datetime(day_data["dteday"])
day_data.set_index("dteday", inplace=True)

# Menampilkan data harian
st.write(day_data)

# Menampilkan statistik data harian
st.write("## Statistik Data Harian")
st.write(day_df.describe())

# Menampilkan data per jam
st.write("## Data Per Jam")
hour_data = hour_df.copy()
st.write(hour_data)

# Menampilkan statistik data per jam
st.write("## Statistik Data Per Jam")
st.write(hour_df.describe())

# Bagian Visualisasi Data
st.write("## Visualisasi Data")

# Pertanyaan 1: Bagaimana total sewa harian dari waktu ke waktu?
st.write("### Pertanyaan 1")
st.write("Bagaimana total sewa harian dari waktu ke waktu?")

# Menyiapkan data untuk total penyewaan harian
day_data["total"] = day_data["casual"] + day_data["registered"]

# Membuat visualisasi dengan Matplotlib untuk total penyewaan harian
fig, ax = plt.subplots(figsize=(10, 6))  # Ukuran gambar
ax.plot(day_data.index, day_data["total"], color="tab:blue")

# Menambahkan label sumbu dan judul
ax.set_xlabel("Date", fontsize=12)
ax.set_ylabel("Count of Rentals", fontsize=12)
ax.set_title("Daily Total Rentals Over Time", fontsize=14)

# Memutar label sumbu X agar tidak tumpang tindih
plt.xticks(rotation=45)

# Menampilkan grafik di Streamlit
st.pyplot(fig)

# Pertanyaan 2: Apakah tren bulanan dan musiman mempengaruhi total penyewaan sepeda?
st.write("### Pertanyaan 2")
st.write("Apakah tren bulanan dan musiman dapat mempengaruhi total penyewaan sepeda?")

# Menyiapkan data bulanan
day_data["month"] = day_data.index.month
monthly_data = day_data.groupby("month")[["total", "casual", "registered"]].sum()
monthly_data.reset_index(inplace=True)
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_data["month"] = monthly_data["month"].map(
    {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
)
monthly_data["month"] = pd.Categorical(monthly_data["month"], categories=month_order, ordered=True)

# Menyiapkan data musiman
day_data["season"] = day_data["season"]
seasonal_data = day_data.groupby("season")[["total", "casual", "registered"]].sum()
seasonal_data.reset_index(inplace=True)
seasonal_data["season"] = seasonal_data["season"].map(
    {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
)

# Membuat subplots dengan 2 kolom (2 grafik sejajar)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Grafik 1: Total penyewaan per bulan
ax1.bar(monthly_data["month"], monthly_data["total"], color='skyblue')
ax1.set_xlabel("Month", fontsize=12)
ax1.set_ylabel("Total Rentals", fontsize=12)
ax1.set_title("Total Bike Rentals by Month", fontsize=14)
ax1.grid(True)

# Grafik 2: Total penyewaan per musim
ax2.bar(seasonal_data["season"], seasonal_data["total"], color='lightgreen')
ax2.set_xlabel("Season", fontsize=12)
ax2.set_ylabel("Total Rentals", fontsize=12)
ax2.set_title("Total Bike Rentals by Season", fontsize=14)
ax2.grid(True)

# Menampilkan grafik di Streamlit
st.pyplot(fig)

# Filter interaktif
# Filter berdasarkan rentang tanggal
st.write("### Filter Berdasarkan Rentang Tanggal")

# Membuat slider untuk memilih rentang tanggal
start_date = st.date_input('Pilih tanggal mulai', day_data.index.min().date())
end_date = st.date_input('Pilih tanggal akhir', day_data.index.max().date())

# Filter data berdasarkan rentang tanggal yang dipilih
if start_date < end_date:
    filtered_data = day_data.loc[start_date:end_date]
    st.write(f"Menampilkan data dari {start_date} hingga {end_date}")
    st.line_chart(filtered_data["total"])
else:
    st.write("Rentang tanggal tidak valid, pastikan tanggal mulai lebih awal dari tanggal akhir.")

# Statistik data per bulan dan musim
# Tabel statistik bulanan
st.write("### Statistik Bulanan")
st.write(monthly_data.describe())

# Tabel statistik musiman
st.write("### Statistik Musiman")
st.write(seasonal_data.describe())

# Analisis Lanjutan dengan Binning
st.write("## Analisis Lanjutan dengan Binning")

temp_bins = [0, 0.2, 0.4, 0.6, 0.8, 1]
hum_bins = [0, 0.3, 0.6, 0.9, 1]
cnt_bins = [0, 500, 1000, 2000, 3000, 5000]

temp_labels = ['Very Low Temp', 'Low Temp', 'Moderate Temp', 'High Temp', 'Very High Temp']
hum_labels = ['Low Humidity', 'Moderate Humidity', 'High Humidity', 'Very High Humidity']
cnt_labels = ['Very Low Rentals', 'Low Rentals', 'Moderate Rentals', 'High Rentals', 'Very High Rentals']

day_df['temp_group'] = pd.cut(day_df['temp'], bins=temp_bins, labels=temp_labels)
day_df['hum_group'] = pd.cut(day_df['hum'], bins=hum_bins, labels=hum_labels)
day_df['cnt_group'] = pd.cut(day_df['cnt'], bins=cnt_bins, labels=cnt_labels)

hour_df['temp_group'] = pd.cut(hour_df['temp'], bins=temp_bins, labels=temp_labels)
hour_df['hum_group'] = pd.cut(hour_df['hum'], bins=hum_bins, labels=hum_labels)
hour_df['cnt_group'] = pd.cut(hour_df['cnt'], bins=cnt_bins, labels=cnt_labels)

# Menampilkan Data Binned Day Dataset
st.write("### Data Harian Setelah Binning")
st.write(day_df[['dteday', 'temp_group', 'hum_group', 'cnt_group']].head())

# Menampilkan Data Binned Hour Dataset
st.write("### Data Per Jam Setelah Binning")
st.write(hour_df[['dteday', 'hr', 'temp_group', 'hum_group', 'cnt_group']].head())
