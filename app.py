from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        youtube_url = request.form.get('url')
        
        if not youtube_url:
            return render_template('index.html', error="Sila masukkan link video!")

        download_url = None

        # Senarai API tempatan/bot serantau yang sangat stabil dan bebas token
        apis = [
            f"https://api.siputzx.my.id/api/d/ytmp3?url={youtube_url}",
            f"https://api.ryzendesu.vip/api/downloader/ytmp3?url={youtube_url}",
            f"https://api.apidown.my.id/api/downloader/ytmp3?url={youtube_url}"
        ]

        # Sistem akan loop dan cuba setiap API satu-persatu
        for api in apis:
            try:
                # Timeout diset pendek (10 saat) supaya kalau server mati, ia cepat lompat ke server lain
                res = requests.get(api, timeout=10)
                if res.status_code == 200:
                    data = res.json()
                    
                    # Struktur fail JSON berbeza ikut penyedia, kita tangkap mana-mana format yang betul
                    download_url = data.get('url') or data.get('data', {}).get('url') or data.get('data', {}).get('dl')
                    
                    if download_url:
                        break # Berjaya dapat link MP3, terus berhenti pusing!
            except:
                continue # Kalau API ni gagal/mati, terus lompat ke API seterusnya tanpa ralat

        # Fallback terakhir (Server ke-4)
        if not download_url:
            try:
                payload = {"url": youtube_url, "downloadMode": "audio", "audioFormat": "mp3"}
                res = requests.post("https://co.wuk.sh/api/json", json=payload, headers={"Accept": "application/json"}, timeout=10)
                if res.status_code == 200:
                    download_url = res.json().get('url')
            except:
                pass

        # Kalau berjaya, terus hantar fail kat kau
        if download_url:
            return redirect(download_url)
        else:
            # Kalau kesemua 4 server mati atau link YouTube salah
            error = "Ralat: Kesemua 4 pelayan pihak ketiga gagal memproses video ini. Sila pastikan link sah dan bukan video 'Live'."

    return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
