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
    startPixel = 1
    for barNr in range(1, barCount + 1):
        animationSpeed = random.randint(600, 1000)
        barCSS += (
            ".bar:nth-child({})  {{ left: {}px; animation-duration: {}ms; }}".format(
                barNr, startPixel, animationSpeed
            )
        )
        startPixel += 4
    return barCSS


def loadImageB64(url):
    return b64encode(requests.get(url).content).decode("ascii")


def makeSVG(data):
    currentlyPlaying = data != {} and data["item"] != "None"
    if currentlyPlaying:
        currentStatus = "🎧  Vibing to"
        item = data["item"]
        # Create the animated bars
        barCount = 81
        animatedBars = "".join(["<div class='bar'></div>" for i in range(barCount)])
        barCSS = barGen(barCount)
    else:
        currentStatus = "🎧  Recently vibed to"
        # get random track from recently played
        recentPlays = recentlyPlayed()
        itemIndex = random.randint(0, len(recentPlays["items"]) - 1)
        item = recentPlays["items"][itemIndex]["track"]
        animatedBars, barCSS = "", ""

    # Get song, artist and coverimage
    songName = item["name"].replace("&", "&amp;")
    artistName = item["artists"][0]["name"].replace("&", "&amp;")
    image = loadImageB64(item["album"]["images"][1]["url"])

    dataDict = {
        "animatedBars": animatedBars,
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
