from flask import Flask, Response

from src.get_data import getNowPlayingSong, getRecentSong
from src.create_widget import create_svg

app = Flask(__name__)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    # retreive data from spotify
    song = getNowPlayingSong()
    if not song:
        song = getRecentSong()

    # generate svg
    if song:
        svg = create_svg(song)
    else:
        svg = "No data found"
    # return response
    return Response(
        svg,
        mimetype="image/svg+xml",
        headers={"Cache-Control": "s-maxage=1"},
    )


if __name__ == "__main__":
    app.run(debug=True)
