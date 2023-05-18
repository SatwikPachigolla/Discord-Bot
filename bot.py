import logging
import json
from gateway_connection import Gateway
# from api import DiscordAPI

class Bot(object):
    def __init__(self, token):
        self.gateway = Gateway(token)
        #self.api = DiscordAPI(token)

    def run_gateway(self):
        self.gateway.run()

    def event(self, f):
        return self.gateway.event(f)

if __name__ == "__main__":
    print("---- Starting up the bot ----")

    config = None
    with open("config.json") as cfg:
        config = json.load(cfg)

    bot = Bot(config["token"])

    @bot.event
    async def ready(x):
        logging.info("The discord gateway connection is ready")

    @bot.event
    async def message_create(msg):
        print(f"Message create event received: {msg}")
        # Look at received message and do whatever you want using it

    bot.run_gateway()
