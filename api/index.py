from flask import Flask, Response

from src.get_data import getCurrentTrack, getRecentTrack
from src.create_svg import create_svg


app = Flask(__name__)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    # retreive data from spotify
    track = getCurrentTrack()
    if not track:
        track = getRecentTrack()

    # generate svg
    svg = create_svg(track)

    # return response
    return Response(
        svg,
        mimetype="image/svg+xml",
        headers={"Cache-Control": "s-maxage=1"},
    )


if __name__ == "__main__":
    app.run(debug=True)
