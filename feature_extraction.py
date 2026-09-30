import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("itunes_cleaned.csv", encoding="utf-8-sig")

# 1. Fitur numerik
menit = df["duration"].str.split(":").str[0].astype(int)
detik = df["duration"].str.split(":").str[1].astype(int)
df["duration_sec"] = menit * 60 + detik
df["song_age"] = 2026 - df["release_year"]
df["title_length"] = df["track_name"].str.len()
df["title_words"] = df["track_name"].str.split().str.len()

# 2. Fitur biner
df["is_single"] = df["album_name"].str.contains("Single", case=False).astype(int)
df["is_collab"] = df["artist_name"].str.contains("&").astype(int)

# 3. One-hot encoding genre
df = pd.concat([df, pd.get_dummies(df["genre"], prefix="genre", dtype=int)], axis=1)

# 4. TF-IDF dari judul lagu
tfidf = TfidfVectorizer()
X = tfidf.fit_transform(df["track_name"])
df_tfidf = pd.DataFrame(X.toarray(), columns=tfidf.get_feature_names_out())
print("Jumlah fitur TF-IDF:", df_tfidf.shape[1])

# 5. Simpan
df.to_csv("itunes_features.csv", index=False, encoding="utf-8-sig")
df_tfidf.to_csv("itunes_tfidf.csv", index=False, encoding="utf-8-sig")

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
print(df[["track_name", "duration_sec", "song_age", "title_length",
          "title_words", "is_single", "is_collab"]])