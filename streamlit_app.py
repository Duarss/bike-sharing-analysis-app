import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Bike Sharing Analysis Dashboard")
st.write(
    "Berikut adalah hasil analisis data sepeda yang dirental sepanjang tahun 2011 sampai 2012."
)

day_df = pd.read_csv("data/day.csv")
hour_df = pd.read_csv("data/hour.csv")

st.write("## Data Harian")
day_data = day_df.copy()
st.write(day_data)

st.write("## Statistik Data Harian")
st.write(day_df.describe())

st.write("## Data Per Jam")
hour_data = hour_df.copy()
st.write(hour_data)

st.write("## Statistik Data Per Jam")
st.write(hour_df.describe())

st.write("## Visualisasi Data")

st.write("### Pertanyaan 1")
st.write("Bagaimana total sewa harian dari waktu ke waktu?")

day_data["dteday"] = pd.to_datetime(day_data["dteday"])
day_data["total"] = day_data["casual"] + day_data["registered"]
day_data.set_index("dteday", inplace=True)
st.line_chart(day_data["total"])

st.write("### Pertanyaan 2")
st.write("Apakah tren bulanan dan musiman dapat mempengaruhi total penyewaan sepeda?")

day_data["month"] = day_data.index.month
monthly_data = day_data.groupby("month").sum()
monthly_data.reset_index(inplace=True)
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_data["month"] = monthly_data["month"].map(
    {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
)
monthly_data["month"] = pd.Categorical(monthly_data["month"], categories=month_order, ordered=True)
monthly_data.set_index("month", inplace=True)
st.bar_chart(monthly_data["total"])

day_data["season"] = day_data["season"]
seasonal_data = day_data.groupby("season").sum()
seasonal_data.reset_index(inplace=True)
seasonal_data["season"] = seasonal_data["season"].map(
    {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
)
seasonal_data.set_index("season", inplace=True)
st.bar_chart(seasonal_data["total"])