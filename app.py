from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Ambil URL tanpa mengira sama ada frontend hantar sebagai JSON atau borang (Form)
            youtube_url = request.json.get('url') if request.is_json else request.form.get('url')
            
            if not youtube_url:
                return jsonify({"error": "Sila masukkan link video atau playlist!"})

            # Panggilan ke Cobalt API
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
                    # Kembalikan link download sebagai JSON yang sah
                    return jsonify({"url": download_url})
                else:
                    return jsonify({"error": "Gagal mendapatkan fail audio. Sila cuba link lain."})
            else:
                return jsonify({"error": "Sistem API sedang sibuk. Sila cuba lagi."})
                
        except Exception as e:
            return jsonify({"error": f"Ralat sistem: {str(e)}"})
            
    # Paparkan halaman HTML hanya jika method adalah GET
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
