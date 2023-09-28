from route.customer import router as customer_router
from fastapi import FastAPI, HTTPException, Request
from app import database
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException


templates = Jinja2Templates(directory="templates")
engine = database.engine

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
# Static config

app.include_router(customer_router)
# Include router


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
# Home page

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=exc.status_code)
# 404 page


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=exc.status_code)
# 404 page

# uvicorn main_demo:app --reload --port 8000
