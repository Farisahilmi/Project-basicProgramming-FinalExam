import pandas as pd
import random 
from datetime import datetime, time

df = pd.read_excel("jadwal_real.xlsx")

daftar_ruangan = ["B4A", "B4B", "B4C", "B4D", "B4E", "B4G", "B4H", "B3A", "B3B", "B3C", "B3D", "B3E", "B3G", "B3H", "B5A", "B5B", "B5C", "B5D", "B5E", "B5G", "B5H"]

df["ruangan"] = [random.choice(daftar_ruangan) for _ in range(len(df))]

df = df[df["Hari"] != "Sabtu"]


df.to_excel("daftar_ruangan.xlsx", index=False)