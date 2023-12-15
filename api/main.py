from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import RedirectResponse
from api import database
from api.route.customer import router as customer_router
from api.route.domain import router as domain_router
from api.route.origin import router as origin_router
from api.route.user import router as user_router
from api import utils, config

templates = Jinja2Templates(directory="api/templates")
engine = database.engine
app = FastAPI()

# Static config
app.mount("/static", StaticFiles(directory="api/static"), name="static")

# Session setting
app.add_middleware(SessionMiddleware, secret_key="some-random-string")




# Include router
app.include_router(domain_router)
app.include_router(origin_router)
app.include_router(user_router)


# Homepage
@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request, db: Session = Depends(utils.get_db)):
    id_user = config.check_session(
        request=request, user_id=request.session.get("id"))
    if id_user:
        return RedirectResponse(url=f"/users/{id_user}/domains", status_code=302)
    return templates.TemplateResponse("admin-home.html", {"request": request})


# 404 page
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=exc.status_code)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=exc.status_code)

# uvicorn main:app --reload --port 8080 --host 0.0.0.0
