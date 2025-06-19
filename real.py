import pandas as pd
import random
from datetime import datetime, time

df = pd.read_excel("jadwal_dosen.xlsx", skiprows=2)
#part satu
df.columns = ["No", "Nama Dosen", "Mata Kuliah", "Semester", "SKS", "Kelas", "Hari", "Jam"]

df = df.dropna(how="all")
df = df.ffill()

df["Hari"] = df["Hari"].str.capitalize()

df = df[df["Hari"].isin(["Senin", "Jumat"])]

daftar_ruangan = ["B4A", "B4B", "B4C", "B4D", "B4E","B4F", "B4G", "B4H", "B3A", "B3B", "B3C", "B3D", "B3E","B3F", "B3G", "B3H", "B5A", "B5B", "B5C", "B5D", "B5E", "B5F", "B5G", "B5H"]

df["Ruangan"] = [random.choice(daftar_ruangan) for _ in range(len(df))]

df[["Mulai", "Selesai"]] = df["Jam"].str.split("-", expand=True)

matakuliah_col = df.pop("Mata Kuliah")

mulai_col = df.pop("Mulai")
Selesai_col = df.pop("Selesai")
hari_col = df.pop("Hari")

df.insert(loc=1, column="Mata Kuliah", value=matakuliah_col)
df.insert(loc=7, column="Mulai", value=mulai_col)
df.insert(loc=8, column="Selesai", value=Selesai_col)
df.insert(loc=0, column="Hari", value=hari_col)

df["Prodi"] = "TI"

df["Mulai"] = df["Mulai"].astype(str).str.strip()
df["Selesai"] = df["Selesai"].astype(str).str.strip()

df = df[df["Mulai"].str.contains(r'^\d{2}.\d{2}$', na=False)]
df = df[df["Selesai"].str.contains(r'\d{2}.\d{2}$', na=False)]

df["Mulai"] = pd.to_datetime(df["Mulai"], format="%H.%M").dt.time
df["Selesai"] = pd.to_datetime(df["Selesai"], format="%H.%M").dt.time

susun_hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]

df["Hari"] = pd.Categorical(df["Hari"], categories=susun_hari, ordered=True)

df = df.sort_values(by=["Hari", "Mulai", "Selesai"]).reset_index(drop=True)
df["Hari"] = df["Hari"].ffill()

df["Kuliah Online atau Offline"] = df["Jam"].apply(lambda x: "Online" if "online" in str(x).lower() else "Offline")

df = df[(df["Mulai"] >= time(8, 0)) & (df["Selesai"] <= time(20, 0))]
df = df[(df["Mulai"] >= time(13, 0 )) | (df["Selesai"] <= time(12, 0))]
df = df[(df["Mulai"] >= time(19, 0)) | (df["Selesai"] <= time(18, 0))]
df = df.drop(columns="No")
df = df.drop(columns="Jam")
#part kedua

df = df[["Hari", "Mata Kuliah", "Nama Dosen", "Kelas", "Ruangan", "Mulai", "Selesai", "SKS", "Semester", "Prodi", "Kuliah Online atau Offline"]]

df.to_excel("farisa.xlsx", index=False)