from starlette.routing import Route

from .views import hello
from .views import main
from .views import private


routes = [
    Route("/", endpoint=main, name="main__main"),
    Route("/hello/{word:str}/", endpoint=hello, name="main__hello"),
    Route("/private/", endpoint=private, name="main__private", methods=["POST", "OPTIONS"]),
]
