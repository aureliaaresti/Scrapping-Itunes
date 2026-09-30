import pandas as pd

df = pd.read_csv("itunes_scraping_result.csv", encoding="utf-8-sig")

# Bersihkan teks HTML
for col in ["html_title", "html_description"]:
    df[col] = (df[col]
               .str.replace("\xa0", " ", regex=False)
               .str.replace("Â", "", regex=False)
               .str.replace(r"\s+", " ", regex=True)
               .str.strip())

# Rapikan teks
for col in ["keyword", "track_name", "artist_name", "album_name"]:
    df[col] = df[col].str.strip()
df["keyword"] = df["keyword"].str.lower()

# Tanggal
df["release_date"] = pd.to_datetime(df["release_date"])
df["release_year"] = df["release_date"].dt.year
df["release_date"] = df["release_date"].dt.date

# Durasi
df["duration"] = df["html_description"].str.extract(r"Duration (\d+:\d+)")

# Hapus duplikat & kosong
df = df.drop_duplicates(subset=["track_name", "artist_name"])
df = df.dropna(subset=["track_name", "artist_name"])

# Buang kolom tidak perlu
df = df.drop(columns=["preview_url", "html_image", "status_code"])

df.to_csv("itunes_cleaned.csv", index=False, encoding="utf-8-sig")
print(df.head())
print("Selesai:", len(df), "baris")