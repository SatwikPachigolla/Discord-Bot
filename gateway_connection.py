import logging
import gateway_utils
import traceback
import platform
from gateway import GatewayCon


# Check https://discord.com/developers/docs/reference#api-versioning for new api versions
GATEWAY_URL = "wss://gateway.discord.gg/?v=10&encoding=json"
NAME = "dicord-bot" # Not sure what this affects
OS = platform.system()
d = None # https://discord.com/developers/docs/topics/gateway-events#heartbeat

'''
Handles creating a websocket connection with Discord's gateway. Implements heartbeating
and handling
'''
class Gateway():

    def __init__(self, token):
        self._token = token
        self._handlers = {}
        self._heartbeat_interval = 1

    def event(self, f):
        self._handlers[f.__name__] = f

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._run_connection())

    async def _run_connection(self):
        logging.info("Running Gateway connection")
        async with websockets.connect(GATEWAY_URL) as ws:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(self._process_loop(ws))
                tg.create_task(self._heartbeat_loop(ws))
            logging.info("Gateway connection closed")

    async def _process_loop(self, ws):
        async for msg in ws:
            unpacked = gateway_utils.json_to_gateway(msg)
            global d
            if unpacked.seq:
                d = unpacked.seq
            try:
                await self.handle_message(ws, unpacked)
            except Exception as e:
                logging.error(f"Exception handling message: {e}")
                traceback.print_exc()

    async def _heartbeat_loop(self, ws):
        while True:
            await asyncio.sleep(self._heartbeat_interval)
            send_heartbeat() # Don't await to avoid adding send time to the heartbeat interval

    async def send(self, ws, msg):
        strmsg = json.dumps(msg)
        logging.debug(f"Gateway message send: {msg}")
        await ws.send(strmsg)

    async def send_heartbeat(self, ws):
        heartbeat = {"op": 1, "d": d}
        await send(ws, json.dumps(heartbeat))

    async def handle_message(self, ws, msg):
        # https://discord.com/developers/docs/topics/opcodes-and-status-codes#gateway-gateway-opcodes
        if msg.op == 0:
            event = msg.event_name.lower()
            if event in self._handlers:
                await self._handlers[event](msg)
            else:
                logging.debug(f"unhandled event: {event}")
        elif msg.op == 1:
            logging.info("Additional heartbeat request received")
            await send_heartbeat(ws)
        elif msg.op == 10:
            logging.info("recieved HELLO")
            self._heartbeat_interval = msg.event_data.heartbeat_interval / 1000 # convert millis to seconds
            identity = { # https://discord.com/developers/docs/topics/gateway-events#identify
                "op": 2,
                "d": {
                    "token": self._token,
                    "properties": { # https://discord.com/developers/docs/topics/gateway-events#identify-identify-connection-properties
                        "os": OS,
                        "browser": NAME,
                        "device": NAME,
                    },
                    "intents": 1 << 12 # https://discord.com/developers/docs/topics/gateway#gateway-intents
                }
            }
            await self.send(identity)
            logging.info("Identify has been sent")
        elif msg.op == 11:
            logging.debug("Heartbeat ack received")
        else:
            raise Exception(f"unknown op: {msg.op}")
