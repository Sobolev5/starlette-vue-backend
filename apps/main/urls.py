from starlette.routing import Route
from starlette.routing import WebSocketRoute

from .views import Chat
from .views import ChatTest1
from .views import ChatTest2
from .views import hello
from .views import main
from .views import private


routes = [
    Route("/", endpoint=main, name="main__main"),
    Route("/hello/{word:str}/", endpoint=hello, name="main__hello"),
    Route("/private/", endpoint=private, name="main__private", methods=["POST", "OPTIONS"]),
    Route("/chat1/", endpoint=ChatTest1, name="main__chat1"),
    Route("/chat2/", endpoint=ChatTest2, name="main__chat2"),
    WebSocketRoute("/chat_ws", Chat),
    WebSocketRoute("/default", Echo),
]
