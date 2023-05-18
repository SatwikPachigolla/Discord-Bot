import asyncio
import websockets
import json
import traceback

from dataclasses import dataclass
from types import SimpleNamespace

import logging as log

class GatewayEvent():

    def __init__(self, op, event_data=None, seq=None, event_name=None):
        self.op = op
        self.event_data = event_data
        self.seq = seq
        self.event_name = event_name

    def __repr__(self):
        return self.__dict__()


def json_to_gateway(msg):
    logging.debug("Unpacking gateway message: %s", msg)

    obj = json.loads(msg)
    op = obj["op"]
    event_data =  obj["d"] if "d" in obj else None
    seq = obj["s"] if "s" in obj else None
    event_name = obj["t"] if "t" in obj else None

    return GatewayEvent(op, event_data, seq, name)

def gateway_to_json(gateway_event):
    logging.debug("Unpacking gateway message: %s", gateway_event)

    msg = {}
    msg["op"] = gateway_event.op
    if gateway_event.event_data:
        msg["d"] = gateway_event.event_data
    if gateway_event.seq:
        msg["s"] = gateway_event.seq
    if gateway_event.event_name:
        msg["t"] = gateway_event.event_name
    return json.dumps(msg)
