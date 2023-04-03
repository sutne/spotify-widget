import os
import requests
import random
from dotenv import load_dotenv, find_dotenv

from src.util import B64_string

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


def getNowPlayingSong() -> dict:
    response = requests.get(
        NOW_PLAYING_URL, headers={"Authorization": f"Bearer {refreshToken()}"}
    )
    if response.status_code == 204:
        return {}
    now_playing = response.json()
    is_playing = (
        now_playing != {}
        and now_playing["item"] != "None"
        and (now_playing["item"]["is_local"] is False)
    )
    item = now_playing["item"]
    return {
        "is_playing": is_playing,
        "title": item["name"],
        "artist": item["artists"][0]["name"],
        "image_url": item["album"]["images"][1]["url"],
        "href": item["external_urls"]["spotify"],
    }


def getRecentSong() -> dict:
    response = requests.get(
        RECENTLY_PLAYING_URL, headers={"Authorization": f"Bearer {refreshToken()}"}
    )
    if response.status_code == 204:
        return {}
    recent_plays = [
        item
        for item in response.json()["items"]
        if item["track"]["is_local"] is not True
    ]
    item = random.choice(recent_plays)["track"]
    return {
        "is_playing": False,
        "title": item["name"],
        "artist": item["artists"][0]["name"],
        "image_url": item["album"]["images"][1]["url"],
        "href": item["external_urls"]["spotify"],
    }
