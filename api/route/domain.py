from fastapi import APIRouter
from fastapi import Depends, Request, Form
from sqlalchemy.orm import Session
from schemas import *
from crud import *
from utils import *
from config import *
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from typing import List

templates = Jinja2Templates(directory="./templates")
router = APIRouter()

@router.get("/users/{user_id}/domains", response_model=List[DomainCreate])
@tracking_time_api
def get_domains(request: Request, user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    id_user = check_session(request=request, user_id=user_id)
    if id_user:
        domains = get_domains(db, user_id=user_id, skip=skip, limit=limit)
        return templates.TemplateResponse("admin-domain.html", {"domains": domains, "user": request.session['username'], "user_id": user_id, "request": request})
    return RedirectResponse(url="/", status_code=302)
# Get domains

@router.get("/users/{user_id}/create-domain", response_class=HTMLResponse)
@tracking_time_api
async def create_domain_get(request: Request, user_id: int):
    id_user = check_session(request=request, user_id=user_id)
    if id_user:
        return templates.TemplateResponse("admin-create-domain.html", {"user_id": user_id, "request": request})
    return RedirectResponse(url="/", status_code=302)
# Create domain form

@router.post("/users/{user_id}/create-domain", response_model=DomainCreate)
@tracking_time_api
def create_domain_post(request: Request, user_id: int, name: str = Form(...), db: Session = Depends(get_db)):
    check_domain = get_domain_by_name(db, name=name)
    if check_domain:
        return templates.TemplateResponse("admin-create-domain.html", {"user_id": user_id, "message": "Domain da ton tai", "request": request})
    domain = create_domain(name=name, user_id=user_id)
    new_domain_id = create_domain(db=db, domain=domain).id
    redirect_url = f"/users/{user_id}/domains/{new_domain_id}/create-origin"
    return RedirectResponse(url=redirect_url, status_code=302)
# Create domain
