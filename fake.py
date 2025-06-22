import pandas as pd
import random
from datetime import datetime, time

# Baca file
df = pd.read_excel("Jadwal_dosen.xlsx", skiprows=2)
df.columns = ["No", "Nama Dosen", "Mata Kuliah", "Semester", "SKS", "Kelas", "Hari", "Jam"]

df = df.dropna(how="all").ffill()
df["Hari"] = df["Hari"].str.capitalize()

# Deteksi Online/Offline
df["Kuliah Online atau Offline"] = df["Jam"].apply(lambda x: "Online" if "online" in str(x).lower() else "Offline")

# Ambil jam bersih
df["Jam Bersih"] = df["Jam"].str.extract(r"(\d{2}\.\d{2}\s*-\s*\d{2}\.\d{2})")[0]
df[["Mulai", "Selesai"]] = df["Jam Bersih"].str.split("-", expand=True)

for col in ["Mulai", "Selesai"]:
    df[col] = df[col].astype(str).str.strip()
    df = df[df[col].str.contains(r'^\d{2}\.\d{2}$', na=False)]
    df[col] = pd.to_datetime(df[col], format="%H.%M").dt.time

# Filter istirahat
istirahat1 = (time(12, 0), time(13, 0))
istirahat2 = (time(18, 0), time(19, 0))
def waktu_valid(start, end):
    return not (
        (istirahat1[0] <= start < istirahat1[1]) or (istirahat1[0] < end <= istirahat1[1]) or
        (istirahat2[0] <= start < istirahat2[1]) or (istirahat2[0] < end <= istirahat2[1])
    )
df = df[df.apply(lambda x: waktu_valid(x["Mulai"], x["Selesai"]), axis=1)]

# Input manual
input_hari = input("Masukkan hari yang ingin disaring (pisahkan dengan koma, contoh: Senin,Jumat): ")
daftar_hari = [h.strip().capitalize() for h in input_hari.split(",") if h.strip()]
df = df[df["Hari"].isin(daftar_hari)]

jam_mulai_user = int(input("Masukkan jam mulai (contoh: 8): "))
jam_selesai_user = int(input("Masukkan jam selesai (contoh: 16): "))
jam_awal = time(jam_mulai_user, 0)
jam_akhir = time(jam_selesai_user, 0)
df = df[df["Mulai"] >= jam_awal]
df = df[df["Selesai"] <= jam_akhir]

# Tambah prodi
df["Prodi"] = "TI"

# Ruangan
daftar_ruangan = [
    "B4A", "B4B", "B4C", "B4D", "B4E", "B4F", "B4G", "B4H",
    "B3A", "B3B", "B3C", "B3D", "B3E", "B3F", "B3G", "B3H",
    "B5A", "B5B", "B5C", "B5D", "B5E", "B5F", "B5G", "B5H"
]
preferensi_Ruang = {
    "TI": [r for r in daftar_ruangan if r.startswith("B4") or r == "B3B"],
    "SI": [r for r in daftar_ruangan if r.startswith("B4") or r.startswith("B3")],
    "DKV": [r for r in daftar_ruangan if r.startswith("B5")],
}

# Alokasi ruang + tandai bentrok
jadwal_terisi = []
ruangan_terpilih = []
status_terpilih = []

def bentrok_jadwal(hari, mulai, selesai, ruangan, nama_dosen, kelas):
    for jadwal in jadwal_terisi:
        if jadwal["Hari"] == hari:
            if max(mulai, jadwal["Mulai"]) < min(selesai, jadwal["Selesai"]):
                if (
                    jadwal["Ruangan"] == ruangan or
                    jadwal["Nama Dosen"] == nama_dosen or
                    jadwal["Kelas"] == kelas
                ):
                    return True
    return False

for _, row in df.iterrows():
    preferensi = preferensi_Ruang.get(row["Prodi"], daftar_ruangan)
    ruang_dapat = None
    for ruang in preferensi:
        if not bentrok_jadwal(row["Hari"], row["Mulai"], row["Selesai"], ruang, row["Nama Dosen"], row["Kelas"]):
            ruang_dapat = ruang
            break
    if ruang_dapat:
        ruangan_terpilih.append(ruang_dapat)
        status_terpilih.append("OK")
        jadwal_terisi.append({
            "Hari": row["Hari"],
            "Mulai": row["Mulai"],
            "Selesai": row["Selesai"],
            "Ruangan": ruang_dapat,
            "Nama Dosen": row["Nama Dosen"],
            "Kelas": row["Kelas"]
        })
    else:
        ruangan_terpilih.append("Bentrok")
        status_terpilih.append("Bentrok")

df["Ruangan"] = ruangan_terpilih
df["Status"] = status_terpilih

# Susun ulang kolom
matakuliah_col = df.pop("Mata Kuliah")
mulai_col = df.pop("Mulai")
selesai_col = df.pop("Selesai")
hari_col = df.pop("Hari")

df.insert(0, "Hari", hari_col)
df.insert(1, "Mata Kuliah", matakuliah_col)
df.insert(7, "Mulai", mulai_col)
df.insert(8, "Selesai", selesai_col)

# Urutkan hari
susun_hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
df["Hari"] = pd.Categorical(df["Hari"], categories=susun_hari, ordered=True)
df = df.sort_values(by=["Hari", "Mulai", "Selesai"]).reset_index(drop=True)

# Simpan ke Excel
df = df.drop(columns=["No", "Jam Bersih"], errors="ignore")
df = df[["Hari", "Mata Kuliah", "Nama Dosen", "Kelas", "Ruangan", "Mulai", "Selesai", "SKS", "Semester", "Prodi", "Kuliah Online atau Offline", "Jam", "Status"]]
df.to_excel("Jadwal_Final.xlsx", index=False)
print("✅ Jadwal lengkap disimpan (termasuk yang bentrok) ke Jadwal_Final.xlsx")
