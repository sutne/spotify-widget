import requests
import base64


def B64_image(url):
    return base64.b64encode(requests.get(url).content).decode("ascii")


def B64_string(str):
    return base64.b64encode(str.encode("ascii")).decode("ascii")
