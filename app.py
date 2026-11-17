from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        youtube_url = request.form.get('url')
        
        if not youtube_url:
            error = "Sila masukkan link video atau playlist!"
            return render_template('index.html', error=error)

        try:
            # Gunakan Cobalt API untuk pintas sekatan YouTube
            api_url = "https://api.cobalt.tools/api/json"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
            payload = {
                "url": youtube_url,
                "isAudioOnly": True,
                "aFormat": "mp3",
                "filenamePattern": "pretty"
            }
            
            res = requests.post(api_url, json=payload, headers=headers)
            
            if res.status_code == 200:
                data = res.json()
                download_url = data.get('url')
                
                if download_url:
                    # Terus bawa pelayar pengguna ke link fail MP3
                    return redirect(download_url)
                else:
                    error = "Gagal mendapatkan fail audio. Sila cuba link lain."
            else:
                error = "Sistem API sedang sibuk atau link tidak disokong. Sila cuba lagi."
                
        except Exception as e:
            error = f"Ralat pelayan: {str(e)}"
            
    return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
