import os
import tempfile
import zipfile
import shutil
from flask import Flask, request, send_file, render_template, jsonify, after_this_request
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'Sila masukkan link YouTube yang sah.'}), 400

    temp_dir = tempfile.mkdtemp()

    # Fungsi untuk buang folder sementara lepas user berjaya download
    @after_this_request
    def cleanup(response):
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            app.logger.error(f"Gagal memadam temp dir: {e}")
        return response

    try:
        # Konfigurasi yt-dlp untuk kualiti MP3 tertinggi
        ydl_opts = {
            'format': 'best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '0', # '0' bermaksud kualiti paling tinggi/original (VBR)
            }],
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'extract_flat': False,
            'ffmpeg_location': './', # Menggunakan FFmpeg yang didownload semasa Render build
            'cookiefile': 'cookies.txt',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Dapatkan maklumat video
            info = ydl.extract_info(url, download=True)
        
        # Semak sama ada link adalah playlist atau single video
        if 'entries' in info:
            # Jika Playlist, kita zipkan semua fail MP3
            zip_filename = f"{info.get('title', 'Playlist_Lagu')}.zip"
            zip_path = os.path.join(temp_dir, zip_filename)
            
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.mp3'):
                            zipf.write(os.path.join(root, file), file)
                            
            return send_file(zip_path, as_attachment=True, download_name=zip_filename)
        
        else:
            # Jika Single Video, cari fail MP3 dan hantar
            for file in os.listdir(temp_dir):
                if file.endswith('.mp3'):
                    file_path = os.path.join(temp_dir, file)
                    return send_file(file_path, as_attachment=True, download_name=file)

        return jsonify({'error': 'Tiada fail MP3 ditemui selepas proses.'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Jalankan server
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
