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

        try:
            # Endpoint rasmi Cobalt v7
            api_url = "https://api.cobalt.tools/"
            
            # Header wajib untuk elak API dari sekat request kita
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Origin": "https://cobalt.tools",
                "Referer": "https://cobalt.tools/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            
            # Parameter format baharu Cobalt v7
            payload = {
                "url": youtube_url,
                "downloadMode": "audio",
                "audioFormat": "mp3",
                "filenamePattern": "pretty"
            }
            
            res = requests.post(api_url, json=payload, headers=headers)
            
            if res.status_code == 200:
                data = res.json()
                download_url = data.get('url')
                
                if download_url:
                    return redirect(download_url)
                else:
                    error = "Gagal menjana link muat turun."
            else:
                # Tangkap ralat SEBENAR dari API supaya kita tahu kalau ada salah
                try:
                    error_msg = res.json().get('error', {}).get('code', res.text)
                except:
                    error_msg = res.text
                error = f"Ditolak oleh API (Kod {res.status_code}): {error_msg}"
                
        except Exception as e:
            error = f"Ralat pelayan: {str(e)}"
            
    return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
