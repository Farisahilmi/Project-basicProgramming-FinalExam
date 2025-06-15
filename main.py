import pandas as pd
import random


df = pd.read_excel("jadwal_dosen.xlsx", sheet_name="angkatan 2024")
df.dropna(how="all")
print(df)