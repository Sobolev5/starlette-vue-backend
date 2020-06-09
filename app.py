from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Mount
from tortoise.contrib.starlette import register_tortoise

from apps.chat.urls import routes as chat_routes
from apps.main.urls import routes as main_routes
from apps.user.urls import routes as user_routes
from middleware import CustomHeaderMiddleware
from middleware import JWTAuthenticationBackend
from settings import DATABASE_URL
from settings import DEBUG
from settings import JWT_ALGORITHM
from settings import JWT_PREFIX
from settings import SECRET_KEY


middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]),
    Middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend(secret_key=str(SECRET_KEY), algorithm=JWT_ALGORITHM, prefix=JWT_PREFIX)),  # str(SECRET_KEY) is important
    Middleware(SessionMiddleware, secret_key=SECRET_KEY),
    Middleware(GZipMiddleware, minimum_size=1000),
    Middleware(CustomHeaderMiddleware),
]


routes = [
    Mount("/chat", routes=chat_routes),
    Mount("/user", routes=user_routes),
    Mount("/", routes=main_routes),
]

entry_point = Starlette(debug=DEBUG, routes=routes, middleware=middleware)


tortoise_models = [
    "apps.user.models",
]

register_tortoise(entry_point, db_url=DATABASE_URL, modules={"models": tortoise_models}, generate_schemas=True)
