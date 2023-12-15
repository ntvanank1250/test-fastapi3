from fastapi import Depends, FastAPI, HTTPException, Request, APIRouter, Form, UploadFile, File
from pydantic import BaseModel
# from rabbitmq import pub
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from api import crud, schemas
from api.utils import *
from api.config import *
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="api/templates")
router = APIRouter()


@router.get("/customers/")
@tracking_time_api
async def read_customers(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return templates.TemplateResponse("customers.html", {"customers": customers, "request": request})
# Get all customers


@router.get("/create-customer/", response_class=HTMLResponse)
@tracking_time_api
async def create_customer(request: Request):
    return templates.TemplateResponse("create-customer.html", {"message_email": '', "message_pass": '', "request": request})
# Create customer form


@router.post("/create-customer/", response_class=HTMLResponse)
@tracking_time_api
async def create_customer(request: Request, email: str = Form(...), password: str = Form(...), repassword: str = Form(...), db: Session = Depends(get_db)):
    db_customer = crud.get_customer_by_email(db, email=email)
    if db_customer:
        return templates.TemplateResponse("create-customer.html", {"message_email": "Email da ton tai", "message_pass": "", "request": request})
    if password != repassword:
        return templates.TemplateResponse("create-customer.html", {"message_email": "", "message_pass": "Re-password is not the same as the password", "request": request})
    newcustomer = schemas.CustomerCreate
    newcustomer.email = email
    newcustomer.password = password
    create_customer = crud.create_customer(db=db, customer=newcustomer)
    return RedirectResponse(url="/customers/", status_code=302)
# Create customer


@router.get("/customers/{customer_id}", response_class=HTMLResponse, response_model=schemas.Customer)
@tracking_time_api
def read_customer(request: Request, customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="customer not found")
    return templates.TemplateResponse("customer.html", {"customer": db_customer, "request": request})
# Get one customer


@router.put("/customers/{customer_id}", response_model=schemas.Customer)
@tracking_time_api
def update_customer(customer_id: int, customer: schemas.Customer, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="customer not found")
    updated_customer = crud.update_customer(
        db, customer_id=customer_id, customer_new=customer)
    return updated_customer
# Put one customer


@router.post("/upload-image-customer/{customer_id}")
@tracking_time_api
async def upload_image(customer_id: int, image: UploadFile = File(...), db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id=customer_id)
    contents = await image.read()
    with open(f"static/images/{image.filename}", "wb") as f:
        f.write(contents)
    upload_image = crud.upload_image_customer(
        db, customer_id=customer_id, image=f"static/images/{image.filename}", list_image=db_customer.image)
    return RedirectResponse(url=f"/customers/{customer_id}", status_code=302)
# Upload image


# @router.post("/purge-cache/{customer_id}")
# async def purge_cache(request: Request, customer_id: int, db: Session = Depends(get_db)):
#     db_customer = crud.get_customer(db, customer_id=customer_id)
#     list_image = db_customer.list_image.split("|")
#     for image in list_image:
#         if image:
#             path_image = "httpGEThieudomain1.com/" + image
#             pub.send_cache_clear_request(path=path_image)
#     pub.send_cache_clear_request(
#         path=f"httpGEThieudomain1.com/customers/{customer_id}")
#     crud.delete_list_image(db, customer_id=customer_id)
#     return RedirectResponse(url=f"/customers/{customer_id}", status_code=302)
# # Purge cache image
