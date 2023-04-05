import dotenv
import requests
import random
import os

from .util import B64_string

dotenv.load_dotenv(dotenv.find_dotenv())
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
