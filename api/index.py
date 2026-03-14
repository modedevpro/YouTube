from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

COOKIE_FILE = "cookies.txt"

@app.route("/")
def home():
    return {"status": "YouTube Info API running"}

@app.route("/info")
def info():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "ضع رابط الفيديو"}), 400

    ydl_opts = {
        "cookiefile": COOKIE_FILE,
        "quiet": True,
        "skip_download": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        data = {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "views": info.get("view_count"),
            "channel": info.get("uploader"),
            "thumbnail": info.get("thumbnail"),
            "download_url": info["url"]
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)