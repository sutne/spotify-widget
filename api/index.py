import os
import random
import requests
from base64 import b64encode
from flask import Flask, Response, render_template
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REFRESH_TOKEN = os.environ.get("SPOTIFY_REFRESH_TOKEN")

REFRESH_TOKEN_URL = "https://accounts.spotify.com/api/token"
NOW_PLAYING_URL = "https://api.spotify.com/v1/me/player/currently-playing"
RECENTLY_PLAYING_URL = "https://api.spotify.com/v1/me/player/recently-played?limit=10"


def getAuth():
    combination = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode("ascii")
    return b64encode(combination).decode("ascii")


def refreshToken():
    data = {
        "grant_type": "refresh_token",
        "refresh_token": SPOTIFY_REFRESH_TOKEN,
    }
    headers = {"Authorization": "Basic {}".format(getAuth())}
    response = requests.post(REFRESH_TOKEN_URL, data=data, headers=headers)
    return response.json()["access_token"]


def nowPlaying():
    headers = {"Authorization": f"Bearer {refreshToken()}"}
    response = requests.get(NOW_PLAYING_URL, headers=headers)
    if response.status_code == 204:
        return {}
    return response.json()


def recentlyPlayed():
    headers = {"Authorization": f"Bearer {refreshToken()}"}
    response = requests.get(RECENTLY_PLAYING_URL, headers=headers)
    if response.status_code == 204:
        return {}
    return response.json()


def addBar(
    barNr,
    startPixel,
    bartype,
    lowSpeed,
    highSpeed,
):
    bar = "<div class='" + bartype + "Bar'></div>"
    animationSpeed = random.randint(lowSpeed, highSpeed)
    barCSS = (
        "."
        + bartype
        + "Bar:nth-child({})  {{ left: {}px; animation-duration: {}ms; }}".format(
            barNr, startPixel, animationSpeed
        )
    )
    return bar, barCSS


def getRandomBarType(barNr):
    # Distribtes base frequencies to the right, and high frequensies to the left.
    if barNr < 15:
        bartype = random.randint(0, 1)
    elif barNr < 75:
        bartype = random.randint(0, 2)
    else:
        bartype = random.randint(1, 2)
    return bartype


def generateBars():
    barCount, startPixel = 90, 1  # barCount has to be a multiple of 3
    bars, barsCSS = "", ""

    barLayout = (
        "position: absolute;"
        "width: 4px;"
        "bottom: 1px;"
        "height: 15px;"
        "background: #21AF43;"
        "border-radius: 1px 1px 0px 0px;"
    )
    bartypes = [("high", 500, 1000), ("medium", 650, 810), ("base", 349, 351)]

    for i in range(1, barCount):
        bartype = getRandomBarType(i)
        newBar, newBarCSS = addBar(
            i,
            startPixel,
            bartypes[bartype][0],
            bartypes[bartype][1],
            bartypes[bartype][2],
        )
        bars += newBar
        barsCSS += newBarCSS
        startPixel += 4

    return barsCSS, barLayout, bars


def loadImageB64(url):
    return b64encode(requests.get(url).content).decode("ascii")


def makeSVG(data):
    currentlyPlaying = (
        data != {} and data["item"] != "None" and (data["item"]["is_local"] is False)
    )
    if currentlyPlaying:
        currentStatus = "🎧  Vibing to"
        item = data["item"]
        # Create the animated bars
        barCSS, barLayout, animatedBars = generateBars()
    else:
        currentStatus = "🎧  Recently vibed to"
        # get random track from recently played, filter away local tracks
        recentPlays = [
            item
            for item in recentlyPlayed()["items"]
            if item["track"]["is_local"] is not True
        ]
        itemIndex = random.randint(0, len(recentPlays) - 1)
        item = recentPlays[itemIndex]["track"]
        animatedBars, barLayout, barCSS = "", "", ""

    # Data that is sent to html
    dataDict = {
        "status": currentStatus,
        "image": loadImageB64(item["album"]["images"][1]["url"]),
        "songName": item["name"].replace("&", "&amp;"),
        "artistName": item["artists"][0]["name"].replace("&", "&amp;"),
        "explicit": item["explicit"],
        # "previewLink": item["preview_url"],
        "trackLink": item["external_urls"]["spotify"],
        # "popularity": item["popularity"],
        "animatedBars": animatedBars,
        "barLayout": barLayout,
        "barCSS": barCSS,
    }
    return render_template("spotify.html.j2", **dataDict)


app = Flask(__name__)


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
