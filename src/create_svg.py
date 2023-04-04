import random
import requests
from base64 import b64encode
from flask import render_template

from .util import B64_image


def create_svg(track: dict | None):
    if not track:
        html_data_dict = {
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
        return render_template("spotify.html.j2", **html_data_dict)

    if track["is_playing"]:
        current_status = "🎧  Currently Listening To"
        # Create the animated bars
        bar_CSS, bar_layout, animated_bars = generate_bars()
    else:
        current_status = "🎧  Recently Listened To"
        # get random track from recently played, filter away local tracks
        animated_bars, bar_layout, bar_CSS = "", "", ""

    # Data that is sent to html
    html_data_dict = {
        "status": current_status,
        "image": B64_image(track["image_url"]),
        "title": track["title"].replace("&", "&amp;"),
        "artist": track["artist"].replace("&", "&amp;"),
        "href": track["href"],
        "animated_bars": animated_bars,
        "bar_layout": bar_layout,
        "bar_CSS": bar_CSS,
    }
    return render_template("spotify.html.j2", **html_data_dict)


def generate_bars():
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
        bartype = get_random_bar_type(i)
        newBar, newBarCSS = add_single_bar(
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


def get_random_bar_type(bar_index):
    # Distributes base frequencies to the right, and high frequencies to the left.
    if bar_index < 15:
        bartype = random.randint(0, 1)
    elif bar_index < 75:
        bartype = random.randint(0, 2)
    else:
        bartype = random.randint(1, 2)
    return bartype


def add_single_bar(
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
