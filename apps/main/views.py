from json import JSONDecodeError

from simple_print.functions import sprint_f
from starlette.authentication import requires
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST

from settings import DEBUG


async def main(request: Request) -> JSONResponse:
    return JSONResponse({"Welcome to starlette-vue": "1"})


async def hello(request: Request) -> JSONResponse:
    word = request.path_params["word"]
    return JSONResponse({"hello": word})


@requires("authenticated")
async def private(request: Request) -> JSONResponse:

    try:
        payload = await request.json()
    except JSONDecodeError:
        sprint_f("cannot_parse_request_body", "red")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="cannot_parse_request_body")

    if DEBUG:
        sprint_f(request.user, "yellow")
        sprint_f(payload, "yellow")

    return JSONResponse(payload)
