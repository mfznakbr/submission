import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


sns.set(style='dark')
url1 = 'https://raw.githubusercontent.com/mfznakbr/submission/main/day.csv'
days_df = pd.read_csv(url1)

url2 = 'https://raw.githubusercontent.com/mfznakbr/submission/main/hour.csv'
hour_df = pd.read_csv(url2)

musim_filter = st.sidebar.selectbox("""
silahkan pilih musim 🥶:\n
1 : Spring \n
2 : Summer \n
3 : Fall \n
4 : Winter""", [1, 2, 3, 4])
jam_filter = st.sidebar.slider("silahkan pilih range jam 🕛:", 0, 23, (6, 18))

# Data Filtering
filtered_df = hour_df[(hour_df["season"] == musim_filter) & 
                      (hour_df["hr"].between(jam_filter[0], jam_filter[1]))]

# Visualisasi
st.title("📊 Dashboard Penyewaan Sepeda")

# Metrik
st.metric("Total Penyewaan", filtered_df["cnt"].sum())
st.metric("Rata-rata Penyewaan", filtered_df["cnt"].mean())

# Barplot Penyewaan per Musim
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="season", y="cnt", data=days_df, estimator=sum, palette="Blues")
ax.set_title("Total Penyewaan Sepeda per Musim")
st.pyplot(fig)

#rata rata
hourly_avg = hour_df.groupby("hr")["cnt"].mean()

# Buat figure dan axis
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(hourly_avg.index, hourly_avg.values, marker="o", linestyle="-", color="b")

# Tambahkan label angka di tiap titik
for i, txt in enumerate(hourly_avg.values):
    ax.annotate(f"{int(txt)}", (hourly_avg.index[i], hourly_avg.values[i]), 
                textcoords="offset points", xytext=(0, 5), ha="center", fontsize=9)

# Atur label dan title
ax.set_title("Rata-rata Penyewaan Sepeda per Jam", fontsize=14)
ax.set_xlabel("Jam", fontsize=12)
ax.set_ylabel("Jumlah Penyewaan", fontsize=12)
ax.set_xticks(range(24))  # Pastikan sumbu X hanya dari 0-23
ax.grid(True, linestyle="--", alpha=0.6)

# Tampilkan di Streamlit
st.pyplot(fig)

st.subheader("🔍 Insight:")
st.write("Penyewaan sepeda paling ramai pada jam sibuk pagi & sore, terutama saat musim Fall atau gugur.")
