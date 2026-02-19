# Developer: محمود عادل الغريب

from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "YouTube API Working ✅"

@app.route("/info")
def video_info():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "Missing url parameter"}), 400

    # مسار ملف الكوكيز داخل مجلد api
    cookies_path = os.path.join(os.path.dirname(__file__), "cookies.txt")

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "nocheckcertificate": True,
        "geo_bypass": True,
        "force_ipv4": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"]
            }
        }
    }

    # لو ملف الكوكيز موجود يضيفه
    if os.path.exists(cookies_path):
        ydl_opts["cookiefile"] = cookies_path

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            downloads = []

            for f in info.get("formats", []):
                if f.get("url") and f.get("vcodec") != "none":
                    downloads.append({
                        "format_id": f.get("format_id"),
                        "ext": f.get("ext"),
                        "resolution": f.get("resolution") or f.get("format_note"),
                        "filesize_mb": round(f.get("filesize", 0) / (1024*1024), 2) if f.get("filesize") else None,
                        "download_url": f.get("url")
                    })

            return jsonify({
                "title": info.get("title"),
                "uploader": info.get("uploader"),
                "duration_seconds": info.get("duration"),
                "views": info.get("view_count"),
                "thumbnail": info.get("thumbnail"),
                "downloads": downloads
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
