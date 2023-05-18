from constants import *
from gateway_protocol import Gateway
from api import DiscordAPI

import logging as log

class Bot(object):
    def __init__(self, token):
        self.gateway = Gateway(token)
        self.api = DiscordAPI(token)

    def run_gateway(self):
        self.gateway.run()

    def event(self, f):
        return self.gateway.event(f)

if __name__ == "__main__":
    print("===  bot startup  ===")

    config = None
    with cfg = open("config.json"):
        config = json.loads(cfg)

    bot = Bot(config["token"])

    @bot.event
    async def ready(x):
        log.info("The discord gateway connection is ready")

    @bot.event
    async def message_create(msg):
        print(f"Message create event received: {msg}")
        # Look at received message and do whatever you want using it

    bot.run_gateway()
