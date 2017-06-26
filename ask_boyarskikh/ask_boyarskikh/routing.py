from channels import route

from app.consumers import questions_connect, questions_disconnect

channel_routing = {
    "websocket.connect": questions_connect,
    "websocket.disconnect": questions_disconnect,
}
