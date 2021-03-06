from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fishbase.fish_logger import set_log_stdout
from fishbase.fish_random import gen_random_str
from pydantic import ValidationError
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.api import api_router
from app.config import config
from app.config.config import API_VERSION
from app.config.config import VERSION
from app.db.session import Session
from app.models.user import CovidUser
from app.schemas.const import VALIDATION_ERROR, ERR_MSG
from app.schemas.errors import CustomException
from app.utils.bloom import BloomFilterUtils

app = FastAPI(title=config.PROJECT_NAME, version=VERSION, openapi_url="/docs/openapi.json")
app.include_router(api_router, prefix=API_VERSION)

# CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def http_middleware(request: Request, call_next):
    request.state.request_tag = gen_random_str(min_length=25, max_length=25)
    request.state.db = Session()
    response = await call_next(request)
    return response


@app.exception_handler(CustomException)
async def exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(custom_response_id=request.state.request_tag)
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "code": "30012",
                "detail": exc.errors(),
                "message": ERR_MSG["30012"],
                "response_id": request.state.request_tag
            }
        ),
    )


def init_bloom_filter():
    bloom_filter = BloomFilterUtils()
    all_user = CovidUser.get_all_user(db=Session())
    for _d in all_user:
        bloom_filter.add(_d.email)


set_log_stdout()
init_bloom_filter()
