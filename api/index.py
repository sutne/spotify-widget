from flask import Flask, Response
from src import get_current_track, get_recent_track, create_svg


app = Flask(__name__)

# since file is called index.py path for this function /api/index.py
# which is automatically routed to /api
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
