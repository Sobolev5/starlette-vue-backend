from starlette.routing import Route
from starlette.routing import WebSocketRoute

from .views import Chat
from .views import ChatTest1
from .views import ChatTest2


routes = [
    Route("/chat1/", endpoint=ChatTest1, name="chat__chat1"),
    Route("/chat2/", endpoint=ChatTest2, name="chat__chat2"),
    WebSocketRoute("/chat_ws", Chat),
]
