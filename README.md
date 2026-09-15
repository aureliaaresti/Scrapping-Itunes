# Tugas Web Scraping — iTunes (HTTP & API)

Scraping data lagu dari **iTunes Search API** dengan dua metode: **API (JSON)** dan
**HTTP/HTML scraping** (BeautifulSoup), masing-masing minimal 10 halaman, sesuai
instruksi tugas Chapter 3 - Web Scraping.

## Struktur file

```
itunes_scraping/
├── itunes_scraping.py   # script utama
├── README.md            # file ini
```

Setelah dijalankan, akan menghasilkan 2 file tambahan:
- `itunes_api_result.csv` — hasil scraping API (10 lagu dari 10 keyword berbeda)
- `itunes_scraping_result.csv` — data API + HTML digabung jadi satu tabel

## Cara pakai

### 1. Install dependency
```bash
pip install requests beautifulsoup4 pandas
```

### 2. Jalankan
```bash
python itunes_scraping.py
```

Atau kalau pakai Google Colab / Jupyter: copy tiap blok kode yang ditandai
`# CELL n` ke cell terpisah, jalankan urut dari atas ke bawah.

## Penjelasan tiap bagian

### CELL 1 — Daftar keyword
10 keyword pencarian (nama artis). **Ganti sesuai topik kelompok kamu** kalau perlu
(genre, judul lagu, dekade tertentu, dll).

### CELL 2 — Scraping API
Request ke endpoint resmi iTunes Search API:
```
https://itunes.apple.com/search?term=<keyword>&media=music&entity=song&limit=1
```
- Gratis, **tidak perlu API key/login**.
- Tiap keyword = 1 request = 1 lagu teratas hasil pencarian → total 10 request
  berbeda memenuhi syarat minimal 10 "halaman" untuk sisi API.
- Data yang diambil: judul lagu, artis, album, tanggal rilis, genre, link preview,
  dan `track_view_url` (dipakai lagi di CELL 3).

### CELL 3 — Scraping HTML
Request ke halaman web lagu di `music.apple.com` (`track_view_url` dari hasil API),
lalu di-parse pakai BeautifulSoup.

**Catatan penting:** halaman `music.apple.com` berat JavaScript, jadi tidak semua
konten yang terlihat di browser ikut terambil lewat `requests` biasa. Yang diambil
di sini adalah **meta tag Open Graph** (`og:title`, `og:description`, `og:image`)
karena tag ini selalu ada di HTML mentah (dipakai untuk preview link di media
sosial), sehingga hasilnya tetap konsisten.

10 lagu dari CELL 2 → 10 URL halaman berbeda → 10 kali `requests.get()` ke HTML,
memenuhi syarat minimal 10 halaman untuk sisi HTTP/HTML.

### CELL 4 — Gabung & simpan
Menggabungkan data API dan data HTML jadi satu tabel (`pandas.DataFrame`), lalu
disimpan ke CSV.

## Etika & batasan scraping

- Ada `time.sleep(1)` di setiap request supaya tidak membebani server (jeda 1
  detik antar request).
- Endpoint iTunes Search API adalah endpoint publik resmi dari Apple, tidak ada
  larangan penggunaan wajar (reasonable use) untuk keperluan non-komersial seperti
  tugas kuliah.
- Kalau kolom `html_title` / `html_description` banyak yang bernilai
  "Tidak ditemukan", kemungkinan halaman tersebut butuh rendering JavaScript penuh
  (di luar cakupan `requests` + `BeautifulSoup` dasar — solusinya perlu tool
  tambahan seperti Selenium, tidak dicakup di script ini).


