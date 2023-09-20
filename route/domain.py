from fastapi import APIRouter
from fastapi import Depends, Request, Form
from sqlalchemy.orm import Session
from app import crud, schemas
import utils, config
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="templates")
router = APIRouter()

# DOMAIN

# Get domains
@router.get("/users/{user_id}/domains", response_model=list[schemas.DomainCreate])
def get_domains(request: Request, user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(utils.get_db)):
    id_user = config.check_session(request=request, user_id=user_id)
    if id_user:
        domains = crud.get_domains(db, user_id=user_id, skip=skip, limit=limit)
        return templates.TemplateResponse("admin-domain.html", {"domains": domains, "user": request.session['username'], "user_id": user_id, "request": request})
    return RedirectResponse(url="/", status_code=302)

# Create domain
@router.get("/users/{user_id}/create-domain", response_class=HTMLResponse)
async def create_domain(request: Request, user_id: int):
    id_user = config.check_session(request=request, user_id=user_id)
    if id_user:
        return templates.TemplateResponse("admin-create-domain.html", {"user_id": user_id, "request": request})
    return RedirectResponse(url="/", status_code=302)

@router.post("/users/{user_id}/create-domain", response_model=schemas.DomainCreate)
def create_domain(request: Request, user_id: int, name: str = Form(...), db: Session = Depends(utils.get_db)):
    check_domain = crud.get_domain_by_name(db, name=name)
    if check_domain:
        return templates.TemplateResponse("admin-create-domain.html", {"user_id": user_id, "message":"Domain da ton tai", "request": request})
    domain =config.create_domain(name=name,user_id=user_id)
    new_domain_id =crud.create_domain(db=db, domain=domain).id
    return templates.TemplateResponse("admin-create-origin.html", {"user_id": user_id, "domain_id": new_domain_id, "request": request})
