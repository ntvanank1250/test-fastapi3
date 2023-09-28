from fastapi import APIRouter
from fastapi import Depends, Request, Form
from sqlalchemy.orm import Session
from app import crud
from utils import *
from config import *
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/logout")
def logout(request: Request):
    session = request.session
    session.clear()
    return templates.TemplateResponse("admin-home.html", {"request": request})
# Logout


@router.get("/sign-in", response_class=HTMLResponse)
async def sign_in(request: Request):
    user_id = check_session(
        request=request, user_id=request.session.get("id"))
    if user_id:
        return RedirectResponse(url=f"/users/{user_id}/domains", status_code=302)
    return templates.TemplateResponse("admin-signin.html", {"request": request})
# Sign-in form


@router.post("/sign-in", response_class=HTMLResponse)
async def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if db_user:
        if db_user.password == password:
            session = request.session
            session["username"] = db_user.name
            session["email"] = db_user.name
            session["id"] = db_user.id
            return RedirectResponse(url=f"/users/{db_user.id}/domains", status_code=302)
        return templates.TemplateResponse("admin-signin.html", {"message_pass": "Sai password", "request": request})
    return templates.TemplateResponse("admin-signin.html", {"message_email": "Email không tồn tại", "request": request})
# Sign-in


@router.get("/sign-up", response_class=HTMLResponse)
async def sign_up(request: Request):
    user_id = check_session(
        request=request, user_id=request.session.get("id"))
    if user_id:
        return RedirectResponse(url=f"/users/{user_id}/domains", status_code=302)
    return templates.TemplateResponse("admin-signup.html", {"request": request})
# Sign-up form


@router.post("/sign-up", response_class=HTMLResponse)
async def sign_up(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...), repassword: str = Form(...), db: Session = Depends(get_db)):
    check_email = crud.get_user_by_email(db, email=email)
    if check_email:
        return templates.TemplateResponse("admin-signup.html", {"message_email": "Email đã tồn tại", "request": request})
    if password != repassword:
        return templates.TemplateResponse("admin-signup.html", {"message_pass": "Pass có giống nhau dell đâu mà tạo được tài khoản", "request": request})
    new_user = create_user(name=name, email=email, password=password)
    crud.create_user(db=db, user=new_user)
    return templates.TemplateResponse("admin-signin.html", {"request": request})
# Sign-up
