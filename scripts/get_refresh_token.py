import os
import base64
import json
from dotenv import load_dotenv, find_dotenv

# Step 1: Load / set environment variables
load_dotenv(find_dotenv())
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI")

if not all([SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI]):
    print("An environment variable was not set")
    exit(0)

# needs privilege to read the following
permissions = ["user-read-currently-playing", "user-read-recently-played"]
SCOPE = ",".join(permissions)

# Step 2: create code
print("Go to the following link:")
code_redirect_url = f"https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&scope={SCOPE}&redirect_uri={SPOTIFY_REDIRECT_URI}"
print(f"\n{code_redirect_url}\n")
url_with_code = input("Paste the URL you are redirected to here: ")
CODE = url_with_code.split("?code=")[1]

combination = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode("ascii")
BASE64 = base64.b64encode(combination).decode("ascii")
command = f'curl -s -X POST -H "Content-Type: application/x-www-form-urlencoded" -H "Authorization: Basic {BASE64}" -d "grant_type=authorization_code&redirect_uri=http://localhost/callback/&code={CODE}" https://accounts.spotify.com/api/token'

# Step 3: Get the refresh token from the json response, copy it to .env file
json_response = json.loads(os.popen(command).read())
print("\n\n" + "\n".join([f"{key}: {value}" for key, value in json_response.items()]))
print("\n\nCopy the refresh_token to your .env file")
