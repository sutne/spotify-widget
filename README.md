# Spotify widget in README.md

<img title="Go to my spotify" src="https://spotify-readme-sivertutne.vercel.app/api/spotify" alt="Nothing currently playing" width="512" />

This was little project i came across when i realised i could have a readme for mye profile. The original is created by [Andrew Novac](https://github.com/novatorem), but i found that the original didn't quite match the way i wanted it, so i customized it a fair bit. The original is as seen below and can be found [here](https://github.com/novatorem/novatorem) with instructions on how to set it up yourself:

[![Spotify](https://novatorem.vercel.app/api/spotify)](https://open.spotify.com/user/omnitenebris)

## Setup

Go to [Spotify for Developers](https://developer.spotify.com/dashboard/applications) and place the following information in a `.env` file in the root of the project:
```sh
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
SPOTIFY_REDIRECT_URI=
```

Run the script `get_refresh_token.py` and add it to your `.env` file:
```sh
SPOTIFY_REFRESH_TOKEN=
```