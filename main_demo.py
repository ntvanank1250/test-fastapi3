from route.customer import router as customer_router
from fastapi import FastAPI, HTTPException, Request, Response
from app import database
import httpx

from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

templates = Jinja2Templates(directory="templates")
engine = database.engine

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
# Static config

app.include_router(customer_router)
# Include router


class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        response.headers["Accept-Range"] = "bytes"
        return response


app.add_middleware(CORSMiddleware, allow_origins=["*"])
app.add_middleware(CustomHeaderMiddleware)

# Home page


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request, response: Response):

    return templates.TemplateResponse("index.html", {"request": request})

# 404 page


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=exc.status_code)

# 404 page


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=exc.status_code)

# uvicorn main_demo:app --reload --port 8000
