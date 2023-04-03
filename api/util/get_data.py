import os
import requests
import random
from dotenv import load_dotenv, find_dotenv

from .util import B64_string

load_dotenv(find_dotenv())
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REFRESH_TOKEN = os.environ.get("SPOTIFY_REFRESH_TOKEN")

REFRESH_TOKEN_URL = "https://accounts.spotify.com/api/token"
NOW_PLAYING_URL = "https://api.spotify.com/v1/me/player/currently-playing"
RECENTLY_PLAYING_URL = "https://api.spotify.com/v1/me/player/recently-played?limit=10"


def refreshToken():
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
    )
    return response.json()["access_token"]


def getCurrentTrack() -> dict | None:
    response = requests.get(
        NOW_PLAYING_URL,
        headers={"Authorization": f"Bearer {refreshToken()}"},
    )

    if not response:
        return None
    if response.status_code != 200:
        return None
    now_playing = response.json()
    if not now_playing or now_playing == {}:
        return None
    if not now_playing["item"]:
        return None
    if now_playing["item"]["is_local"]:
        return None

    item = now_playing["item"]
    return {
        "is_playing": True,
        "title": item["name"],
        "artist": item["artists"][0]["name"],
        "image_url": item["album"]["images"][1]["url"],
        "href": item["external_urls"]["spotify"],
    }


def getRecentTrack() -> dict | None:
    response = requests.get(
        RECENTLY_PLAYING_URL,
        headers={"Authorization": f"Bearer {refreshToken()}"},
    )

    if not response:
        return None
    if response.status_code != 200:
        return None
    recent_tracks = response.json()["items"]
    if not recent_tracks:
        return None
    if recent_tracks == {}:
        return None

    recent_tracks = [item for item in recent_tracks if not item["track"]["is_local"]]
    item = random.choice(recent_tracks)["track"]
    return {
        "is_playing": False,
        "title": item["name"],
        "artist": item["artists"][0]["name"],
        "image_url": item["album"]["images"][1]["url"],
        "href": item["external_urls"]["spotify"],
    }
