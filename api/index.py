import random


###################################################################### Endpoint
from flask import Flask, Response


app = Flask(__name__)

# since file is called widget.py path for this function /api/widget
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):

    # retreive data from spotify
    track = get_current_track()
    if not track:
        track = get_recent_track()

    # generate svg
    svg = create_svg(track)

    # return response
    return Response(
        svg,
        mimetype="image/svg+xml",
        headers={"Cache-Control": "s-maxage=1"},
    )


###################################################################### data
from dotenv import load_dotenv, find_dotenv
import requests
import os

load_dotenv(find_dotenv())
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REFRESH_TOKEN = os.environ.get("SPOTIFY_REFRESH_TOKEN")

REFRESH_TOKEN_URL = "https://accounts.spotify.com/api/token"
NOW_PLAYING_URL = "https://api.spotify.com/v1/me/player/currently-playing"
RECENTLY_PLAYING_URL = "https://api.spotify.com/v1/me/player/recently-played?limit=50"


def get_token():
    AUTHORIZATION = B64_string(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}")
    response = requests.post(
        REFRESH_TOKEN_URL,
        headers={
            "Authorization": f"Basic {AUTHORIZATION}",
        },
        data={
            "grant_type": "refresh_token",
            "refresh_token": SPOTIFY_REFRESH_TOKEN,
        },
    ).json()
    return response["access_token"]


def get_current_track():
    result = requests.get(
        NOW_PLAYING_URL,
        headers={"Authorization": f"Bearer {get_token()}"},
    )

    if not result:
        return None
    if result.status_code != 200:
        return None
    response = result.json()
    if not response or response == {}:
        return None
    if not response["item"]:
        return None
    if response["item"]["is_local"]:
        return None

    track = response["item"]
    return {
        "is_playing": True,
        "title": track["name"],
        "artist": ", ".join([artist["name"] for artist in track["artists"]]),
        "image_url": track["album"]["images"][1]["url"],
        "href": track["external_urls"]["spotify"],
    }


def get_recent_track():
    result = requests.get(
        RECENTLY_PLAYING_URL,
        headers={"Authorization": f"Bearer {get_token()}"},
    )

    if not result:
        return None
    if result.status_code != 200:
        return None
    response = result.json()
    if not response or response == {}:
        return None
    if not response["items"]:
        return None

    items = [item for item in response["items"] if not item["track"]["is_local"]]
    track = random.choice(items)["track"]

    return {
        "is_playing": False,
        "title": track["name"],
        "artist": ", ".join([artist["name"] for artist in track["artists"]]),
        "image_url": track["album"]["images"][1]["url"],
        "href": track["external_urls"]["spotify"],
    }


###################################################################### svg
from flask import render_template


def create_svg(track):
    if not track:
        svg_data_dict = {
            "is_playing": False,
            "status": "No songs found",
            "image": B64_image(
                "https://img.freepik.com/free-icon/browser_318-313458.jpg"
            ),
            "title": "404",
            "artist": "Song Not Found",
            "href": "https://open.spotify.com/",
            "animated_bars": "",
            "bar_layout": "",
            "bar_CSS": "",
        }
        return render_template("spotify.html.j2", **svg_data_dict)

    if track["is_playing"]:
        current_status = "🎧  Currently Listening To"
        # Create the animated bars
        bar_CSS, bar_layout, animated_bars = create_bars()
    else:
        current_status = "🎧  Recently Listened To"
        # get random track from recently played, filter away local tracks
        animated_bars, bar_layout, bar_CSS = "", "", ""

    # Data that is sent to html
    svg_data_dict = {
        "is_playing": track["is_playing"],
        "status": current_status,
        "image": B64_image(track["image_url"]),
        "title": track["title"].replace("&", "&amp;"),
        "artist": track["artist"].replace("&", "&amp;"),
        "href": track["href"],
        "animated_bars": animated_bars,
        "bar_layout": bar_layout,
        "bar_CSS": bar_CSS,
    }
    return render_template("spotify.html.j2", **svg_data_dict)


def create_bars():
    bar_count, start_pixel = 90, 1  # barCount has to be a multiple of 3
    bars, bars_CSS = "", ""

    bar_layout = (
        "position: absolute;"
        "width: 4px;"
        "bottom: 1px;"
        "height: 15px;"
        "background: #21AF43;"
        "border-radius: 1px 1px 0px 0px;"
    )
    bar_types = [("high", 500, 1000), ("medium", 650, 810), ("base", 349, 351)]

    for bar_number in range(1, bar_count):
        bar_type = get_bar_type(bar_number)
        new_bar, new_bar_CSS = create_bar(
            bar_number,
            start_pixel,
            bar_types[bar_type][0],
            bar_types[bar_type][1],
            bar_types[bar_type][2],
        )
        bars += new_bar
        bars_CSS += new_bar_CSS
        start_pixel += 4

    return bars_CSS, bar_layout, bars


def get_bar_type(bar_index):
    # Distributes base frequencies to the right, and high frequencies to the left.
    if bar_index < 15:
        bar_type = random.randint(0, 1)
    elif bar_index < 75:
        bar_type = random.randint(0, 2)
    else:
        bar_type = random.randint(1, 2)
    return bar_type


def create_bar(
    bar_number,
    start_pixel,
    bar_type,
    low_speed,
    high_speed,
):
    bar = f"<div class='{bar_type}Bar'/>"
    animation_speed = random.randint(low_speed, high_speed)
    bar_CSS = f"""
    .{bar_type}Bar:nth-child({bar_number}) {{ 
        left: {start_pixel}px; 
        animation-duration: {animation_speed}ms; 
    }}"""
    return bar, bar_CSS


###################################################################### util
import base64


def B64_image(url):
    return base64.b64encode(requests.get(url).content).decode("ascii")


def B64_string(str):
    return base64.b64encode(str.encode("ascii")).decode("ascii")
