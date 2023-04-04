from base64 import b64encode
import requests


def B64_image(url: str):
    return b64encode(requests.get(url).content).decode("ascii")


def B64_string(str: str):
    return b64encode(str.encode("ascii")).decode("ascii")
