from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route("/download", methods=["GET"])
def download():

    video_url = request.args.get("url")

    if not video_url:
        return {"error": "ضع الرابط هكذا ?url=رابط_الفيديو"}, 400

    cookies = {
        'PHPSESSID': 'se7of57ehbf0fcunhg7fiqiiqc',
        '_ga': 'GA1.1.1310491172.1771357265',
        '_ga_2K69M9RN1B': 'GS2.1.s1771357265$o1$g0$t1771357330$j60$l0$h0',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://app.ytdown.to',
        'priority': 'u=1, i',
        'referer': 'https://app.ytdown.to/en2/',
        'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'url': video_url,
    }

    response = requests.post(
        'https://app.ytdown.to/proxy.php',
        cookies=cookies,
        headers=headers,
        data=data
    )

    # يرجع الرد فقط بدون status_code
    return Response(response.text, content_type=response.headers.get("Content-Type"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)