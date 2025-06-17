import pandas as pd

df = pd.read_excel("mapping_matakuliah/Jadwal_TI24.xlsx")
df = df[df["Kelas"].str.contains("TI24T")]

df = df.dropna(how="all")
baris_baru = {
    "No": [6, 7],
    "Nama Dosen": ["Dr.Jasmansyah, M.Pd", "Sona Minasyan, MSW"],
    "Mata Kuliah": ["Pendidikan Pancasila", "Bahasa Inggris Profesi"],
    "Semester": [1, 1],
    "SKS": [2,2],
    "Kelas": ["TI24T", "TI24T"],
    "Hari": ["Daring", "Daring"],
    "Jam": ["10.00 - 12.30", "10.00 - 12.30"],
    "Kuliah Online atau Offline": ["Online", "Online"],
}

df["No"] = range(1, len(df) + 1)
df = pd.concat([df, pd.DataFrame(baris_baru)], ignore_index=True)
print(df)
df.to_excel("ti24.xlsx", index=False)
