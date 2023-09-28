from route.customer import router as customer_router
from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from app import database
from route.domain import router as domain_router
from route.origin import router as origin_router
from route.user import router as user_router
import utils
import config
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import RedirectResponse


templates = Jinja2Templates(directory="templates")
engine = database.engine
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
# Static config

app.add_middleware(SessionMiddleware, secret_key="some-random-string")
# Session setting

app.include_router(domain_router)
app.include_router(origin_router)
app.include_router(user_router)
# Include router


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request, db: Session = Depends(utils.get_db)):
    id_user = config.check_session(
        request=request, user_id=request.session.get("id"))
    if id_user:
        return RedirectResponse(url=f"/users/{id_user}/domains", status_code=302)
    return templates.TemplateResponse("admin-home.html", {"request": request})
# Homepage


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=exc.status_code)
# 404 page


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=exc.status_code)
# 404 page

# uvicorn main:app --reload --port 8080
