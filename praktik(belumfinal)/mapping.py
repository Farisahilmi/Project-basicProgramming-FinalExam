import pandas as pd

df = pd.read_excel("jadwal_dosen.xlsx", skiprows=2)

df.columns = ["No", "Nama Dosen", "Mata Kuliah", "Semester", "SKS", "Kelas", "Hari", "Jam"]
df.dropna(how="all")
df = df.fillna(method="ffill")
df["Kuliah Online atau Offline"] = df["Jam"].apply(lambda x: "Online" if "online" in str(x).lower() else "Offline")

df_TI_24 = df[df["Kelas"].str.contains("24")]
df_TI_23 = df[df["Kelas"].str.contains("23")]
df_TI_22 = df[df["Kelas"].str.contains("22")]

df_TI_24.to_excel("mapping_matakuliah/Jadwal_TI24.xlsx", index=False)
df_TI_23.to_excel("mapping_matakuliah/Jadwal_TI23.xlsx", index=False)
df_TI_22.to_excel("mapping_matakuliah/jadwal_TI22.xlsx", index=False)
df.to_excel("mapping_matakuliah/jadwal_baru.xlsx", index=False)