from flask import Flask, Response

from src.get_data import getNowPlayingSong, getRecentSong
from src.create_widget import create_svg

app = Flask(__name__)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    # retreive data from spotify
    nowPlayingSong = getNowPlayingSong()
    recentSong = getRecentSong()
    if nowPlayingSong["is_playing"]:
        song = nowPlayingSong
    else:
        song = recentSong
    # generate svg
    svg = create_svg(song)
    # return response
    return Response(
        svg,
        mimetype="image/svg+xml",
        headers={"Cache-Control": "s-maxage=1"},
    )


if __name__ == "__main__":
    app.run(debug=True)
