import pandas as pd

df = pd.read_excel("mapping_matakuliah/jadwal_baru.xlsx")


df = df.sort_values(by="Semester", ascending=True)


df[["Mulai", "Selesai"]] = df["Jam"].str.split("-", expand=True)
mulai_col = df.pop("Mulai")
selesai_col = df.pop("Selesai")
hari_col = df.pop("Hari")

df.insert(loc=7, column="Mulai", value=mulai_col)
df.insert(loc=8, column="Selesai", value=selesai_col)
df.insert(loc=0, column="Hari", value=hari_col)

df = df.drop(columns=["Jam"])
df = df.drop(columns=["No"])
print(df.columns.tolist())

df.to_excel("main.xlsx")
