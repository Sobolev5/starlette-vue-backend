import jwt
from simple_print.functions import sprint_f
from starlette.authentication import AuthCredentials
from starlette.authentication import AuthenticationBackend
from starlette.authentication import AuthenticationError
from starlette.authentication import BaseUser
from starlette.middleware.base import BaseHTTPMiddleware

from settings import DEBUG


class JWTUser(BaseUser):
    def __init__(self, username: str, user_id: int, email: str, token: str, **kw) -> None:
        self.username = username
        self.user_id = user_id
        self.email = email
        self.token = token

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.username

    def __str__(self) -> str:
        return f"JWT user: username={self.username}, id={self.user_id}, email={self.email}"


class JWTAuthenticationBackend(AuthenticationBackend):
    def __init__(self, secret_key: str, algorithm: str = "HS256", prefix: str = "Bearer"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.prefix = prefix

    @classmethod
    def get_token_from_header(cls, authorization: str, prefix: str):

        if DEBUG:
            sprint_f(f"JWT token from headers: {authorization}", "cyan")  # debug part, do not forget to remove it
        try:
            scheme, token = authorization.split()
        except ValueError:
            if DEBUG:
                sprint_f(f"Could not separate Authorization scheme and token", "red")
            raise AuthenticationError("Could not separate Authorization scheme and token")
        if scheme.lower() != prefix.lower():
            if DEBUG:
                sprint_f(f"Authorization scheme {scheme} is not supported", "red")
            raise AuthenticationError(f"Authorization scheme {scheme} is not supported")
        return token

    async def authenticate(self, request):

        if "Authorization" not in request.headers:
            return None

        authorization = request.headers["Authorization"]
        token = self.get_token_from_header(authorization=authorization, prefix=self.prefix)

        try:
            jwt_payload = jwt.decode(token, key=str(self.secret_key), algorithms=self.algorithm)
        except jwt.InvalidTokenError:
            if DEBUG:
                sprint_f(f"Invalid JWT token", "red")
            raise AuthenticationError("Invalid JWT token")
        except jwt.ExpiredSignatureError:
            if DEBUG:
                sprint_f(f"Expired JWT token", "red")
            raise AuthenticationError("Expired JWT token")

        if DEBUG:
            sprint_f(f"Decoded JWT payload: {jwt_payload}", "green")  # debug part, do not forget to remove it

        return (
            AuthCredentials(["authenticated"]),
            JWTUser(username=jwt_payload["username"], user_id=jwt_payload["user_id"], email=jwt_payload["email"], token=token),
        )


class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["starlette-vue"] = "1"
        return response
