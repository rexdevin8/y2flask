#app.py
from flask import Flask, request, send_file, render_template, redirect
from pytube import YouTube
import logging
import sys
import os
from io import BytesIO
from tempfile import TemporaryDirectory
import gunicorn

print("Server is running :)")
print(".....................")

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
app = Flask(__name__)


@app.route("/audio")
def download_audio():
    youtube_url = request.args.get('url')
    print(youtube_url)

    with TemporaryDirectory() as tmp_dir:
        print(tmp_dir)
        yt = YouTube(str(youtube_url))
        audio = yt.streams.get_audio_only()
        download_path = audio.download(tmp_dir)

        base, ext = os.path.splitext(download_path)
        new_file = base + '.mp3'
        try:
            os.rename(download_path, new_file)
        except:
            pass

        faudio_name = new_file.split("\\")[-1]
        print(download_path)
        print(faudio_name)
        hpath, audio_name = os.path.split(faudio_name)
        print("filename is : " + audio_name)
        file_bytes = b""
        with open(new_file, "rb") as f:
            file_bytes = f.read()

        return send_file(BytesIO(file_bytes), attachment_filename=audio_name, as_attachment=True)

if __name__ == "__main__":
    app.run(threaded=True, port=5000)
