import requests
import logging
# Unused
'''
DISCORD_API="https://discord.com/api"

def handle_api_response(resp):
    resp.raise_for_status()
    try:
        body = resp.json()
        if "errors" in body:
            raise Exception(f"{body}")
        return body
    except:
        return resp.text

class DiscordAPI(object):
    def __init__(self, token):
        log.info("init Discord REST API")
        self._token = token

    def make_get_request(self, path):
        resp = requests.get(_http_url(path), headers=_headers())
        return handle_api_response(resp)

    def make_put_request(self, path):
        resp = requests.put(_http_url(path), headers=_headers())
        return handle_api_response(resp)

    def make_post_request(self, path, body):
        resp = requests.post(_http_url(path), headers=_headers(), body=body)
        return handle_api_response(resp)

    def _http_url(path):
        return f"{DISCORD_API}{path}"

    def _headers():
        return {
                "Authorization": f"Bot {self._token}",
        }
'''
