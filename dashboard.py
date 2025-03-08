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

# fungsi filter data
def data_filter(hour_df, season, hour_range):
    if season == 0:  # Jika user memilih "All Seasons"
        return hour_df[hour_df["hr"].between(hour_range[0], hour_range[1])]
    return hour_df[(hour_df["season"].isin(season)) & (hour_df["hr"].between(hour_range[0], hour_range[1]))]

# fungsi mendapatkan ringkasan per musim
def get_musim(filtered_df):
    seasonal_summary = filtered_df.groupby('season')['cnt'].agg(['sum', 'mean']).reset_index()
    seasonal_summary.columns = ['season', 'total_rentals', 'average_rentals']
    return seasonal_summary

# fungsi mendapatkan ringkasan per jam
def get_hourly_summary(filtered_df):
    hourly_summary = filtered_df.groupby("hr")["cnt"].agg(["sum", "mean"]).reset_index()
    hourly_summary.columns = ["hr", "total_rentals", "average_rentals"]
    return hourly_summary

# Load data
days_df, hour_df = data_load()

# 🔹 Sidebar Filtering
st.sidebar.header("🔍 Filter Data")
musim_filter = st.sidebar.multiselect(
    "Silahkan pilih musim 🌤️:", 
    [0, 1, 2, 3, 4], 
    default=[0],  # Default pilih "All Seasons"
    format_func=lambda x: 
        "All Seasons" if x == 0 else 
        "Spring" if x == 1 else
        "Summer" if x == 2 else
        "Fall" if x == 3 else
        "Winter" 
)

jam_filter = st.sidebar.slider("Silahkan pilih range jam ⏰:", 0, 23, (6, 18))

# 🔹 Filter Data
if 0 in musim_filter:
    filtered_df = data_filter(hour_df, list(range(1, 5)), jam_filter)  # Semua musim jika "All Seasons" dipilih
else:
    filtered_df = data_filter(hour_df, musim_filter, jam_filter)

# 🔹 Dashboard Title
st.title("📊 Dashboard Penyewaan Sepeda")

# 🔹 Metrics
st.metric("Total Penyewaan", filtered_df["cnt"].sum())
st.metric("Rata-rata Penyewaan", filtered_df["cnt"].mean())

# 🔹 Update Ringkasan Data
seasonal_summary = get_musim(filtered_df)
hourly_summary = get_hourly_summary(filtered_df)

# 🔹 Barplot Total & Rata-rata Penyewaan per Musim
fig, ax = plt.subplots(1, 2, figsize=(16, 8))

sns.barplot(x="season", y="total_rentals", data=seasonal_summary, color='#17BECF', ax=ax[0])
ax[0].set_title("Total Penyewaan Sepeda per Musim")

sns.barplot(x="season", y="average_rentals", data=seasonal_summary, color='#FFC20A', ax=ax[1])
ax[1].set_title("Rata-rata Penyewaan Sepeda per Musim")

st.pyplot(fig)

# 🔹 Line Chart Rata-rata Penyewaan Sepeda per Jam
fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(hourly_summary["hr"], hourly_summary["average_rentals"], marker="o", linestyle="-", color="b")

for i, txt in enumerate(hourly_summary["average_rentals"]):
    ax.annotate(f"{int(txt)}", (hourly_summary["hr"][i], hourly_summary["average_rentals"][i]), 
                textcoords="offset points", xytext=(0, 5), ha="center", fontsize=9)

ax.set_title("Rata-rata Penyewaan Sepeda per Jam", fontsize=14)
ax.set_xlabel("Jam", fontsize=12)
ax.set_ylabel("Jumlah Penyewaan", fontsize=12)
ax.set_xticks(range(24))
ax.grid(True, linestyle="--", alpha=0.6)

st.pyplot(fig)

# 🔹 Line Chart Total Penyewaan Sepeda per Jam
fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(hourly_summary["hr"], hourly_summary["total_rentals"], marker="s", linestyle="--", color="r")

for i, txt in enumerate(hourly_summary["total_rentals"]):
    ax.annotate(f"{int(txt)}", (hourly_summary["hr"][i], hourly_summary["total_rentals"][i]), 
                textcoords="offset points", xytext=(0, 5), ha="center", fontsize=9)

ax.set_title("Total Penyewaan Sepeda per Jam", fontsize=14)
ax.set_xlabel("Jam", fontsize=12)
ax.set_ylabel("Jumlah Penyewaan", fontsize=12)
ax.set_xticks(range(24))
ax.grid(True, linestyle="--", alpha=0.6)

st.pyplot(fig)

# 🔹 Insight
st.subheader("🔍 Insight:")
# Fungsi untuk mengubah angka musim menjadi teks
def format_musim(x):
    return (
        "All Seasons" if x == 0 else
        "Spring" if x == 1 else
        "Summer" if x == 2 else
        "Fall" if x == 3 else
        "Winter"
    )

# Menggunakan fungsi format_musim untuk menampilkan teks musim yang dipilih
selected_seasons_text = (
    "semua musim" if 0 in musim_filter 
    else ", ".join([format_musim(x) for x in musim_filter])
)

st.write(f"Penyewaan sepeda paling ramai pada jam sibuk pagi & sore, terutama saat musim {selected_seasons_text}.")
