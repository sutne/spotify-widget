# Spotify Widget

> Widget shows my currently playing track on spotify, or selects randomly from my 20 most recently played tracks.

<img src="https://spotify-widget-sutne.vercel.app/api" alt="Currently having some techincal difficulties 😅" width="508" height="173" />

---

The original is created by [Andrew Novac](https://github.com/novatorem) as seen below and can be found [here](https://github.com/novatorem/novatorem).
​
[![Spotify](https://novatorem.vercel.app/api/spotify)](https://open.spotify.com/user/omnitenebris)


# Spotify Setup

### Creating Spotify Developer App

1. Go to [Spotify for Developers](https://developer.spotify.com/dashboard/applications) 
2. Create a new app, call it whetever you want.

### Getting Required Tokens

1. Go to the settings of the created Spotify App
2. For the field `Redirect URI` place an arbitrary localhost URL, such as `http://localhost/callback/`
3. Create a `.env` file in the root of the project
4. Fill the `.env` file with the the following fields (all are foun don the spotify app settings page)

```
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
SPOTIFY_REDIRECT_URI=
```

5. Run the script `get_refresh_token.py`after following the instructions you should have received your `refresh token`. This token never expires so make sure to keep it safe.
6. Add the token to the `.env` file

```
SPOTIFY_REFRESH_TOKEN=
```

# Vercel Setup

### Creating Vercel Project

1. Create and account/login to [vercel.com](https://vercel.com), i reccomend signing in using your GitHub account.
2. Install `vercel` using your prefferred package manager:

```sh
yarn add global vercel
```
```sh
npm install -g vercel
```
3. From the root of the project you should now be able to use `vercel` to set up and configure the project.
```sh
vercel
``` 
4. Add the environment variables from the `.env` file the vercel project in its settings.

### Developing
Simply use the following command from the root:
```sh
vercel dev
```

### Deploying Changes

To Deploy changes manually you can use:
```sh
vercel --prod
```
You can also link the project with a branch in a github repo to automatically deploy the most recent version.