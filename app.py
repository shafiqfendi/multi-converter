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

        # Senarai pelayan komuniti Cobalt yang tidak perlukan token JWT
        api_instances = [
            "https://api.cobalt.my.id/",
            "https://cobalt.qewertyy.dev/",
            "https://cobalt-api.peppe8o.com/",
            "https://co.wuk.sh/"
        ]
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        
        # Gabungan parameter untuk sokong kedua-dua versi Cobalt (v6 dan v7)
        payload = {
            "url": youtube_url,
            "downloadMode": "audio",    # Parameter v7
            "audioFormat": "mp3",       # Parameter v7
            "isAudioOnly": True,        # Parameter v6
            "aFormat": "mp3",           # Parameter v6
            "filenamePattern": "pretty"
        }
        
        berjaya = False
        
        # Sistem akan loop dan cuba satu-satu server sampai dapat
        for api_url in api_instances:
            try:
                # Tambah timeout supaya tak tunggu lama sangat kalau server tu mati
                res = requests.post(api_url, json=payload, headers=headers, timeout=10)
                
                if res.status_code == 200:
                    data = res.json()
                    download_url = data.get('url')
                    
                    if download_url:
                        berjaya = True
                        return redirect(download_url)
            except:
                # Kalau pelayan ni gagal/timeout, abaikan dan cuba pelayan seterusnya
                continue
                
        if not berjaya:
            error = "Semua pelayan bantuan sedang sibuk. Sila cuba lagi sebentar lagi."
            
    return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
