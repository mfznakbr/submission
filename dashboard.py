import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


sns.set(style='dark')

# dataset 
def data_load():
    dayurl = 'https://raw.githubusercontent.com/mfznakbr/submission/main/day.csv'
    hoururl = 'https://raw.githubusercontent.com/mfznakbr/submission/main/hour.csv'
    
    days_df = pd.read_csv(dayurl)
    hour_df = pd.read_csv(hoururl)
    return days_df, hour_df
    

# dataframe musim
def get_musim(days_df):
    seasonal_summary = days_df. groupby('season')['cnt'].agg(['sum', 'mean']).reset_index()
    seasonal_summary.columns = ['season', 'total_rentals', 'average_rentals']
    return seasonal_summary


def data_filter(hour_df, season, hour_range):
    return hour_df[(hour_df["season"] == season) & (hour_df["hr"].between(hour_range[0], hour_range[1]))]

def get_hourly_summary(hour_df):
    hourly_summary = hour_df.groupby("hr")["cnt"].agg(["sum", "mean"]).reset_index()
    hourly_summary.columns = ["hr", "total_rentals", "average_rentals"]
    return hourly_summary

days_df, hour_df = data_load()

# filter untuk sidebar
musim_filter = st.sidebar.selectbox("""
silahkan pilih musim 🥶:\n
1 : Spring \n
2 : Summer \n
3 : Fall \n
4 : Winter""", [1, 2, 3, 4])
jam_filter = st.sidebar.slider("silahkan pilih range jam 🕛:", 0, 23, (6, 18))

# untuk filter data
filtered_df = data_filter(hour_df, musim_filter, jam_filter)
seasonal_summary = get_musim(days_df)
hourly_summary = get_hourly_summary(hour_df)

# Dashboard Title
st.title("📊 Dashboard Penyewaan Sepeda")

# metrik
st.metric("Total Penyewaan", filtered_df["cnt"].sum())
st.metric("Rata-rata Penyewaan", filtered_df["cnt"].mean())

# Barplot Total & Rata-rata Penyewaan per Musim
fig, ax = plt.subplots(1, 2, figsize=(14, 5))

# Total Penyewaan per Musim
sns.barplot(x="season", y="total_rentals", data=seasonal_summary, palette="Blues", ax=ax[0])
ax[0].set_title("Total Penyewaan Sepeda per Musim")

# Rata-rata Penyewaan per Musim
sns.barplot(x="season", y="average_rentals", data=seasonal_summary, palette="Oranges", ax=ax[1])
ax[1].set_title("Rata-rata Penyewaan Sepeda per Musim")

st.pyplot(fig)

# 🔹 Line Chart Rata-rata Penyewaan Sepeda per Jam
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(hourly_summary["hr"], hourly_summary["average_rentals"], marker="o", linestyle="-", color="b")

# Tambahkan label angka di tiap titik
for i, txt in enumerate(hourly_summary["average_rentals"]):
    ax.annotate(f"{int(txt)}", (hourly_summary["hr"][i], hourly_summary["average_rentals"][i]), 
                textcoords="offset points", xytext=(0, 5), ha="center", fontsize=9)

ax.set_title("Rata-rata Penyewaan Sepeda per Jam", fontsize=14)
ax.set_xlabel("Jam", fontsize=12)
ax.set_ylabel("Jumlah Penyewaan", fontsize=12)
ax.set_xticks(range(24))
ax.grid(True, linestyle="--", alpha=0.6)

st.pyplot(fig)  # ⬅️ Menampilkan grafik pertama

# 🔹 Line Chart Total Penyewaan Sepeda per Jam
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(hourly_summary["hr"], hourly_summary["total_rentals"], marker="s", linestyle="--", color="r")

# Tambahkan label angka di tiap titik
for i, txt in enumerate(hourly_summary["total_rentals"]):
    ax.annotate(f"{int(txt)}", (hourly_summary["hr"][i], hourly_summary["total_rentals"][i]), 
                textcoords="offset points", xytext=(0, 5), ha="center", fontsize=9)

ax.set_title("Total Penyewaan Sepeda per Jam", fontsize=14)
ax.set_xlabel("Jam", fontsize=12)
ax.set_ylabel("Jumlah Penyewaan", fontsize=12)
ax.set_xticks(range(24))
ax.grid(True, linestyle="--", alpha=0.6)

st.pyplot(fig)  # ⬅️ Menampilkan grafik kedua (di bawah grafik pertama)

# Insights
st.subheader("🔍 Insight:")
st.write("Penyewaan sepeda paling ramai pada jam sibuk pagi & sore, terutama saat musim gugur.")
