# Developer: محمود عادل الغريب

from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/info")
def video_info():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "Missing url parameter"}), 400

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "nocheckcertificate": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"]
            }
        }
    }

    # لو cookies.txt موجود
    if os.path.exists("cookies.txt"):
        ydl_opts["cookiefile"] = "cookies.txt"

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

            data = {
                "title": info.get("title"),
                "uploader": info.get("uploader"),
                "duration_seconds": info.get("duration"),
                "views": info.get("view_count"),
                "thumbnail": info.get("thumbnail"),
                "downloads": downloads
            }

            return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
