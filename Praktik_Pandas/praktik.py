
import pandas as pd

df = pd.DataFrame({
    "Mulai": ["08.00", "8.00", "13:00", "10.30", "08.00 ", "jam 09.00"]
})

df_valid = df[df["Mulai"].str.contains(r'^\d{2}\.\d{2}$', na=False)]

print(df_valid)