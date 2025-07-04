from flask import Flask, render_template, request, send_file, flash, redirect
import yt_dlp
import os
import uuid

app = Flask(__name__)

 app.secret_key = 'your_secret_key'
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['url']
        try:
            unique_id = str(uuid.uuid4())
            output_template = os.path.join(DOWNLOAD_FOLDER, f'{unique_id}.%(ext)s')

            ydl_opts = {
                'outtmpl': output_template,
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'quiet': True,
                'noplaylist': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info).replace('.webm', '.mp4').replace('.mkv', '.mp4')

            flash("Download successful!", "success")
            return send_file(filename, as_attachment=True)

        except Exception as e:
            flash(f"Error: {str(e)}", "danger")

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug = True)
