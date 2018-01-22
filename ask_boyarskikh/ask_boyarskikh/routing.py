# pylint: disable=invalid-name

from channels.routing import route  # pylint: disable=unused-import

from app.consumers import ws_connect, ws_disconnect

channel_routing = {
    'websocket.connect': ws_connect,
    'websocket.disconnect': ws_disconnect,
}
