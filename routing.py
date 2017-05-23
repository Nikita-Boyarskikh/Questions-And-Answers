from channels import route

from questions.consumers import questions_connect, questions_disconnect

channel_routing = [
    route("websocket.connect", questions_connect, path=r'^/questions/events/$'),

    route("websocket.disconnect", questions_disconnect, path=r'^/questions/events/$'),
]
