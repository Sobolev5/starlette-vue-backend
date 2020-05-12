from starlette.routing import Route

from .views import refresh_token
from .views import user_login
from .views import user_register


routes = [
    Route("/register", endpoint=user_register, methods=["POST", "OPTIONS"], name="user__register"),
    Route("/login", endpoint=user_login, methods=["POST", "OPTIONS"], name="user__login"),
    Route("/refresh-token/", endpoint=refresh_token, methods=["POST", "OPTIONS"], name="user__refresh_token"),
]
