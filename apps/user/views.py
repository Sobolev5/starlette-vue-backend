from datetime import datetime
from datetime import timedelta
from json import JSONDecodeError

import jwt
from passlib.hash import pbkdf2_sha256
from starlette.authentication import requires
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST
from user_agents import parse

from ..mailer.mailer import Mailer
from .models import User
from settings import JWT_ALGORITHM
from settings import JWT_PREFIX
from settings import PROJECT_MAIL
from settings import SECRET_KEY
from settings import USE_MAILER

# A library to identify devices (phones, tablets) and parse it


async def create_token(token_config: dict) -> str:

    exp = datetime.utcnow() + timedelta(minutes=token_config["expiration_minutes"])
    token = {
        "username": token_config["username"],
        "user_id": token_config["user_id"],
        "email": token_config["email"],
        "iat": datetime.utcnow(),
        "exp": exp,
    }

    if "get_expired_token" in token_config:
        token["sub"] = "token"
    else:
        token["sub"] = "refresh_token"

    token = jwt.encode(token, str(SECRET_KEY), algorithm=JWT_ALGORITHM)
    return token.decode("UTF-8")


async def user_register(request: Request) -> JSONResponse:

    try:
        payload = await request.json()
    except JSONDecodeError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Can't parse json request")

    username = payload["username"]
    email = payload["email"]
    password = pbkdf2_sha256.hash(payload["password"])

    user_exist = await User.filter(email=email).first()
    if user_exist:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Already registred")

    new_user = User()
    new_user.username = username
    new_user.email = email
    new_user.password = password
    await new_user.save()

    if USE_MAILER == True:
        mailer_message = Mailer(
            sender=PROJECT_MAIL,
            recipient_list=(f"{email}"),
            subject="You are registered on the Project!",
            letter_body=f"You are welcome {username}! You are now registered. <br> Your login: {email} <br> Thank you for registering on our site.",
        )
        mailer_message.send_email()
    else:
        pass

    token = await create_token({"email": email, "username": username, "user_id": new_user.id, "get_expired_token": 1, "expiration_minutes": 30})
    refresh_token = await create_token({"email": email, "username": username, "user_id": new_user.id, "get_refresh_token": 1, "expiration_minutes": 10080})

    return JSONResponse({"id": new_user.id, "username": new_user.username, "email": new_user.email, "token": f"{JWT_PREFIX} {token}", "refresh_token": f"{JWT_PREFIX} {refresh_token}",}, status_code=200,)


async def user_login(request: Request) -> JSONResponse:

    # Parsing of user-agent characteristic string
    try:
        ua_string = request.headers.get("User-Agent", "<unknown>")
    except:
        ua_string = None
    if ua_string:
        user_agent = parse(ua_string)
        user_agent = str(user_agent)

    try:
        payload = await request.json()
    except JSONDecodeError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Can't parse json request")

    email = payload["email"]
    password = payload["password"]

    user = await User.filter(email=email).first()
    if user:
        if pbkdf2_sha256.verify(password, user.password):
            user.last_login_date = datetime.now()
            await user.save()

            if USE_MAILER == True:
                mailer_message = Mailer(
                    sender=PROJECT_MAIL, recipient_list=(f"{user.email}"), subject="You are logged to the Project!", letter_body=f"You are welcome {user.username}! Today at {datetime.now()} you entered the site from: <br> {user_agent}.",
                )
                mailer_message.send_email()
            else:
                pass

            token = await create_token({"email": user.email, "username": user.username, "user_id": user.id, "get_expired_token": 1, "expiration_minutes": 30})
            refresh_token = await create_token({"email": user.email, "username": user.username, "user_id": user.id, "get_refresh_token": 1, "expiration_minutes": 10080})

            return JSONResponse({"id": user.id, "username": user.username, "email": user.email, "token": f"{JWT_PREFIX} {token}", "refresh_token": f"{JWT_PREFIX} {refresh_token}",}, status_code=200,)
        else:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Invalid login or password")
    else:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Invalid login or password")


@requires("authenticated")
async def refresh_token(request: Request) -> JSONResponse:

    # Here you can add blacklist (aioredis)
    # and user data reload (for example if username was changed)

    username = request.user.username
    user_id = request.user.user_id
    email = request.user.email

    token = await create_token({"email": email, "username": username, "user_id": user_id, "get_expired_token": 1, "expiration_minutes": 30})
    refresh_token = await create_token({"email": email, "username": username, "user_id": user_id, "get_refresh_token": 1, "expiration_minutes": 10080})

    return JSONResponse({"id": user_id, "username": username, "email": email, "token": f"{JWT_PREFIX} {token}", "refresh_token": f"{JWT_PREFIX} {refresh_token}",}, status_code=200,)
