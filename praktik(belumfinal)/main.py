import pandas as pd

df = pd.read_excel("main.xlsx")

df = df[["Hari", "Mulai", "Selesai", "Mata Kuliah", "Kelas", "Nama Dosen"]].copy()

df["Prodi"] = "TI"


df["Mulai"] = df["Mulai"].astype(str).str.strip()
df["Selesai"] = df["Selesai"].astype(str).str.strip()

df = df[df["Mulai"].str.contains(r'^\d{2}\.\d{2}$', na=False)]
df = df[df["Selesai"].str.contains(r'^\d{2}\.\d{2}$', na=False)]

df["Mulai"] = pd.to_datetime(df["Mulai"], format="%H.%M").dt.time
df["Selesai"] = pd.to_datetime(df["Selesai"], format="%H.%M").dt.time

susun_hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
df["Hari"] = df["Hari"].str.capitalize()
df["Hari"] = pd.Categorical(df["Hari"], categories=susun_hari, ordered=True)

df_susun = df.sort_values(by=["Hari", "Mulai", "Selesai"]).reset_index(drop=True)
df_susun["Hari"] = df_susun["Hari"].ffill()
print(df_susun)

df_susun.to_excel("Jadwal_real.xlsx", index=False)