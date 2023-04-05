import flask
import random

from .util import B64_image


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
        return flask.render_template("spotify.html.j2", **svg_data_dict)

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
    return flask.render_template("spotify.html.j2", **svg_data_dict)


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
