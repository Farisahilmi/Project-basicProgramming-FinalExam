#import pandas alias statment pd
#import random
#dari datetime import datetime, time
import pandas as pd
import random
from datetime import datetime, time

#baca file dengan format pd.read_excel "baca excel([Namafile])"
df = pd.read_excel("Jadwal_dosen.xlsx", skiprows=2)
df.columns = ["No", "Nama Dosen", "Mata Kuliah", "Semester", "SKS", "Kelas", "Hari", "Jam"]

df = df.dropna(how="all")
df = df.ffill()
df["Hari"] = df["Hari"].str.capitalize()

df[["Mulai", "Selesai"]] = df["Jam"].str.split("-", expand=True)
for col in ["Mulai", "Selesai"]:
    df[col] = df[col].astype(str).str.strip()
    df = df[df[col].str.contains(r'^\d{2}.\d{2}$', na=False)]
    df[col] = pd.to_datetime(df[col], format="%H.%M").dt.time

istirahat1 = (time(12, 0), time(13, 0))
istirahat2 = (time(18, 0), time(19, 0))
def waktu_valid(start, end):
    return not (
        (istirahat1[0] <= start < istirahat1[1]) or (istirahat1[0] < end <= istirahat1[1]) or
        (istirahat2[0] <= start < istirahat2[1]) or (istirahat2[0] < end <= istirahat2[1])
    )
    
df = df[df.apply(lambda x: waktu_valid(x["Mulai"], x["Selesai"]), axis=1)]

#input hari dengan manual
input_hari = input("masukan hari yang ingin disaring (pisahkan dengan koma, contoh: Senin,Jumat): ")
daftar_hari = [h.strip().capitalize() for h in input_hari.split(",") if h.strip()]

df = df[df["Hari"].isin(daftar_hari)]

jam_mulai_user = int(input("Masukkan jam mulai (contoh: 8): "))
jam_selesai_user = int(input("masukkan jam selesai (contoh: 16): "))

jam_awal = time(jam_mulai_user, 0)
jam_akhir = time(jam_selesai_user, 0)
df = df[df["Mulai"] >= jam_awal]
df = df[df["Selesai"] <= jam_akhir]



df["Prodi"] = "TI"

daftar_ruangan = ["B4A", "B4B", "B4C", "B4D", "B4E","B4F", "B4G", "B4H", "B3A", "B3B", "B3C", "B3D", "B3E","B3F", "B3G", "B3H", "B5A", "B5B", "B5C", "B5D", "B5E", "B5F", "B5G", "B5H"]

preferensi_Ruang = {
    "TI": [r for r in daftar_ruangan if r.startswith("B4") or r.startswith("B3B")],
    "SI": [r for r in daftar_ruangan if r.startswith("B4") or r.startswith("B3")],
    "DKV": [r for r in daftar_ruangan if r.startswith("B5")],
}

jadwal_terisi = []
def cari_ruangan_tersedia(hari, mulai, selesai, preferensi):
    for ruang in preferensi:
        bentrok = False
        for jadwal in jadwal_terisi:
            if jadwal["Hari"] == hari and jadwal["Ruangan"] == ruang:
                if max(mulai, jadwal["Mulai"]) < min(selesai, jadwal["Selesai"]):
                    bentrok = True
                    break
        if not bentrok:
            return ruang
    return None # tidak ada ruangan yang cocok

ruangan_terpilih = []
for index, row in df.iterrows():
    preferensi = preferensi_Ruang.get(row["Prodi"], daftar_ruangan)
    ruang = cari_ruangan_tersedia(row["Hari"], row["Mulai"], row["Selesai"], preferensi)
    if ruang:
        ruangan_terpilih.append(ruang)
        jadwal_terisi.append({
            "Hari": row["Hari"],
            "Mulai": row["Mulai"],
            "Selesai": row["Selesai"],
            "Ruangan": ruang
        })
    else:
        ruangan_terpilih.append("Bentrok Jadwalnya")
        
df["Ruangan"] = ruangan_terpilih

df["Kuliah Online atau Offline"] = df["Jam"].apply(lambda x: "Online" if "online" in str(x).lower() else "Offline")

matakuliah_col = df.pop("Mata Kuliah")
mulai_col = df.pop("Mulai")
Selesai_col = df.pop("Selesai")
hari_col = df.pop("Hari")

df.insert(loc=1, column="Mata Kuliah", value=matakuliah_col)
df.insert(loc=7, column="Mulai", value=mulai_col)
df.insert(loc=8, column="Selesai", value=Selesai_col)
df.insert(loc=0, column="Hari", value=hari_col)

susun_hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
df["Hari"] = pd.Categorical(df["Hari"], categories=susun_hari, ordered=True)
df = df.sort_values(by=["Hari", "Mulai", "Selesai"]).reset_index(drop=True)

def cek_bentrok(df):
    konflik = []
    for i, row1 in df.iterrows():
        for j, row2 in df.iterrows():
            if i >= j: continue
            if row1["Hari"] == row2["Hari"] and max(row1["Mulai"], row2["Mulai"]) < min(row1["Selesai"], row2["Selesai"]):
                if row1["Nama Dosen"] == row2["Nama Dosen"] or row1["Kelas"] == row2["Kelas"] or row1["Ruangan"] == row2["Ruangan"]:
                    konflik.append((i, j))
    return konflik

bentrok = cek_bentrok(df)
if bentrok:
    print("Ada bentrok: ", bentrok)
                
else:
    df = df.drop(columns=["No", "Jam"], errors="ignore")
    df = df[["Hari", "Mata Kuliah", "Nama Dosen", "Kelas", "Ruangan", "Mulai", "Selesai", "SKS", "Semester", "Prodi", "Kuliah Online atau Offline"]]
    df.to_excel("Jadwal_Final.xlsx", index=False)
    print("Jadwal berhasil")