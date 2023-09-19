from fastapi import APIRouter
from fastapi import Depends, Request, Form
from sqlalchemy.orm import Session
from app import crud, schemas, redis_connecttion
import utils, config
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="templates")

router = APIRouter()

# ORIGIN

# Get origins
@router.get("/users/{user_id}/domains/{domain_id}/origins", response_model=list[schemas.OriginCreate])
def get_domains(request: Request, user_id: int, domain_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(utils.get_db)):
    id_user = config.check_session(request=request,user_id = user_id)
    if id_user:
        origins = crud.get_origins(db, domain_id=domain_id, skip=skip, limit=limit)
        r = redis_connecttion.get_redis_connection()
        id_domain_default = 0
        id_domain_default = int(r.get("id_domain"))
        return templates.TemplateResponse("admin-origin.html", {"origins": origins, "user": request.session['username'], "user_id": user_id, "domain_id": domain_id, "id_domain_default":id_domain_default, "request": request})
    return RedirectResponse(url="/", status_code=302)

# Get origin
@router.get("/users/{user_id}/domains/{domain_id}/origins/{origin_id}", response_model=list[schemas.OriginCreate])
async def get_data_origin(request: Request, user_id: int, domain_id: int, origin_id: int, db: Session = Depends(utils.get_db)):
    id_user = config.check_session(request=request,user_id = user_id)
    if id_user:
        origin = crud.get_origin(db=db, origin_id=origin_id)
        key = str(origin.domain.name)
        value = str(origin.protocol) + '|' + str(origin.upstr_host) + '|' + str(origin.upstr_address)
        r = redis_connecttion.get_redis_connection()
        r.delete(key)
        r.set(key, value)
        r.set("id_domain", origin_id)
        return RedirectResponse(f"/users/{user_id}/domains/{domain_id}/origins", status_code=302)
    return RedirectResponse(url="/", status_code=302)

# Create origin
@router.get("/users/{user_id}/domains/{domain_id}/create-origin", response_class=HTMLResponse)
async def create_origin(request: Request, user_id: int, domain_id: int):
    id_user = config.check_session(request=request, user_id=user_id)
    if id_user:
        return templates.TemplateResponse("admin-create-origin.html", {"user_id": user_id, "domain_id": domain_id, "request": request})
    return RedirectResponse(url="/", status_code=302)

@router.post("/users/{user_id}/domains/{domain_id}/create-origin", response_model=schemas.OriginCreate)
def create_origin(request: Request, user_id: int, domain_id: int, name: str = Form(...), upstr_host: str = Form(...), upstr_address: str = Form(...), protocol: str = Form(...), db: Session = Depends(utils.get_db)):
    origin = config.create_origin(name=name,upstr_host=upstr_host,upstr_address=upstr_address,protocol=protocol,domain_id=domain_id)
    crud.create_origin(db=db, origin=origin)
    return RedirectResponse(url=f"/users/{user_id}/domains/{domain_id}/origins", status_code=302)