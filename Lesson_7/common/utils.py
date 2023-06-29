import json
from decos import log

from common.variables import MAX_PACK_LEN, ENCODING


@log
def get_message(sock):
    encoded_response = sock.recv(MAX_PACK_LEN)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


@log
def send_message(sock, message):
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
