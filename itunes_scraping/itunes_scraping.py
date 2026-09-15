"""
Tugas: Web Scraping - HTTP dan API
Target: iTunes Search API (music.apple.com)
Metode: API scraping (JSON) + HTTP/HTML scraping (BeautifulSoup)
Minimal 10 halaman untuk masing-masing metode.

Cara pakai:
    pip install requests beautifulsoup4 pandas
    python itunes_scraping.py

Atau copy tiap blok (dipisah komentar "CELL n") ke cell terpisah di Google Colab / Jupyter Notebook.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


# ============================================
# CELL 1: Keyword pencarian (bisa diganti sesuai topik kelompok)
# ============================================
keywords = [
    'bruno major',
    'taylor swift',
    'raisa',
    'tulus',
    'bruno mars',
    'the weeknd',
    'bernadya',
    'perunggu',
    'Hivi',
    'pamungkas'
]


# ============================================
# CELL 2: BAGIAN API - request ke iTunes Search API (JSON)
# Setiap keyword = 1 request API = 1 "halaman" API
# ============================================
def scrape_api(keywords):
    song_list = []

    for kw in keywords:
        url = f'https://itunes.apple.com/search?term={kw.replace(" ", "+")}&media=music&entity=song&limit=1'
        res = requests.get(url)
        print(f"[API] {kw} -> status {res.status_code}")

        data = res.json()

        if data.get('results'):
            s = data['results'][0]
            song_list.append({
                'keyword': kw,
                'track_name': s.get('trackName'),
                'artist_name': s.get('artistName'),
                'album_name': s.get('collectionName'),
                'release_date': s.get('releaseDate'),
                'genre': s.get('primaryGenreName'),
                'preview_url': s.get('previewUrl'),
                'track_view_url': s.get('trackViewUrl'),
            })

        time.sleep(1)  # jeda sopan antar request

    return song_list


# ============================================
# CELL 3: BAGIAN HTTP/HTML - scrape halaman detail tiap lagu
# Setiap lagu = 1 halaman HTML berbeda = total 10 halaman
# ============================================
def scrape_html(song_list):
    hasil_html = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    for i, song in enumerate(song_list):
        url = song.get('track_view_url')
        print(f"[HTML] Scraping halaman {i + 1}/{len(song_list)}: {url}")

        if not url:
            hasil_html.append({
                'url': None, 'status_code': 'Skip (no url)',
                'html_title': None, 'html_description': None, 'html_image': None
            })
            continue

        try:
            page = requests.get(url, headers=headers)
            bs = BeautifulSoup(page.text, 'html.parser')

            # ambil dari meta tag Open Graph (og:), lebih stabil daripada elemen
            # visual karena halaman iTunes berat JavaScript
            og_title = bs.find('meta', property='og:title')
            og_description = bs.find('meta', property='og:description')
            og_image = bs.find('meta', property='og:image')

            hasil_html.append({
                'url': url,
                'status_code': page.status_code,
                'html_title': og_title['content'] if og_title else 'Tidak ditemukan',
                'html_description': og_description['content'] if og_description else 'Tidak ditemukan',
                'html_image': og_image['content'] if og_image else 'Tidak ditemukan',
            })
        except Exception as e:
            hasil_html.append({
                'url': url, 'status_code': 'Error',
                'html_title': str(e), 'html_description': None, 'html_image': None
            })

        time.sleep(1)

    return hasil_html


# ============================================
# CELL 4: Gabungin data API + HTML, simpan ke CSV
# ============================================
def main():
    song_list = scrape_api(keywords)
    df_api = pd.DataFrame(song_list)
    df_api.to_csv('itunes_api_result.csv', index=False)
    print(f"\n[OK] Data API tersimpan: itunes_api_result.csv ({len(df_api)} baris)\n")

    hasil_html = scrape_html(song_list)

    df_final = pd.DataFrame(song_list)
    df_final['html_title'] = [h['html_title'] for h in hasil_html]
    df_final['html_description'] = [h['html_description'] for h in hasil_html]
    df_final['html_image'] = [h['html_image'] for h in hasil_html]
    df_final['status_code'] = [h['status_code'] for h in hasil_html]

    df_final.to_csv('itunes_scraping_result.csv', index=False)
    print(f"[OK] Data gabungan (API + HTML) tersimpan: itunes_scraping_result.csv ({len(df_final)} baris)")

    print("\n--- Preview hasil ---")
    print(df_final.head(10).to_string())


if __name__ == '__main__':
    main()
