import os
import random
import requests
from base64 import b64encode
from dotenv import load_dotenv, find_dotenv
from flask import Flask, Response, render_template

load_dotenv(find_dotenv())

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET_ID = os.getenv("SPOTIFY_SECRET_ID")
SPOTIFY_REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")
REFRESH_TOKEN_URL = "https://accounts.spotify.com/api/token"
NOW_PLAYING_URL = "https://api.spotify.com/v1/me/player/currently-playing"
RECENTLY_PLAYING_URL = "https://api.spotify.com/v1/me/player/recently-played?limit=10"

app = Flask(__name__)


def getAuth():
    return b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_SECRET_ID}".encode()).decode("ascii")


def refreshToken():
    data = {
        "grant_type": "refresh_token",
        "refresh_token": SPOTIFY_REFRESH_TOKEN,
    }
    headers = {"Authorization": "Basic {}".format(getAuth())}
    response = requests.post(REFRESH_TOKEN_URL, data=data, headers=headers)
    return response.json()["access_token"]


def recentlyPlayed():
    headers = {"Authorization": f"Bearer {refreshToken()}"}
    response = requests.get(RECENTLY_PLAYING_URL, headers=headers)

    if response.status_code == 204:
        return {}
    return response.json()


def nowPlaying():
    headers = {"Authorization": f"Bearer {refreshToken()}"}
    response = requests.get(NOW_PLAYING_URL, headers=headers)

    if response.status_code == 204:
        return {}
    return response.json()


def barGen(barCount):
    barCSS = ""
    left = 1
    for i in range(1, barCount + 1):
        anim = random.randint(600, 1000)
        barCSS += (
            ".bar:nth-child({})  {{ left: {}px; animation-duration: {}ms; }}".format(
                i, left, anim
            )
        )
        left += 4
    return barCSS


def loadImageB64(url):
    resposne = requests.get(url)
    return b64encode(resposne.content).decode("ascii")


def makeSVG(data):
    barCount = 81
    contentBar = "".join(["<div class='bar'></div>" for i in range(barCount)])
    barCSS = barGen(barCount)

    if data == {} or data["item"] == "None":
        # No song is currently playing
        contentBar = ""
        currentStatus = "🎧  Recently vibed to"
        recentPlays = recentlyPlayed()
        itemIndex = random.randint(0, len(recentPlays["items"]) - 1)
        item = recentPlays["items"][itemIndex]["track"]
    else:
        item = data["item"]
        currentStatus = "🎧  Vibing to"
    image = loadImageB64(item["album"]["images"][1]["url"])
    artistName = item["artists"][0]["name"].replace("&", "&amp;")
    songName = item["name"].replace("&", "&amp;")

    dataDict = {
        "contentBar": contentBar,
        "barCSS": barCSS,
        "artistName": artistName,
        "songName": songName,
        "image": image,
        "status": currentStatus,
    }
    return render_template("spotify.html.j2", **dataDict)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    data = nowPlaying()
    svg = makeSVG(data)
    resp = Response(svg, mimetype="image/svg+xml")
    resp.headers["Cache-Control"] = "s-maxage=1"
    return resp


if __name__ == "__main__":
    app.run(debug=True)
