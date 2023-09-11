from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
import uvicorn
from app import crud, models, schemas, database
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import PlainTextResponse
from starlette.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles


templates = Jinja2Templates(directory="templates")

SessionLocal = database.SessionLocal
engine = database.engine

models.Base.metadata.create_all(bind=engine)

# app1 basic + frontend
app_server = FastAPI()

# Đường dẫn tới thư mục chứa các tệp tĩnh
app_server.mount("/static", StaticFiles(directory="static"), name="static")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# homepage


@app_server.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
# end homepage


### Customers

# get customers
@app_server.get("/customers/", response_class=HTMLResponse, response_model=list[schemas.Customer])
def read_customers(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), ):
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return templates.TemplateResponse("customers.html", {"customers": customers, "request": request})

# create  customer

@app_server.post("/Customers/create-customer", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = crud.get_customer_by_email(db, email=customer.email)
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_customer(db=db, customer=customer)

# get a customer


@app_server.get("/customers/{customer_id}", response_class=HTMLResponse, response_model=schemas.Customer)
def read_customer(request: Request, customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return templates.TemplateResponse("customer.html", {"customer": db_customer, "request": request})

# put customer


@app_server.put("/customers/{customer_id}", response_model=schemas.Customer)
def update_customer(customer_id: int, customer: schemas.Customer, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="customer not found")

    updated_customer = crud.update_customer(db, customer_id=customer_id, customer_new=customer)
    return updated_customer

# change pass customer


@app_server.put("/customers/{customer_id}/change_pass", response_model=schemas.ChangePassword)
def change_pass(customer_id: int, customer: schemas.ChangePassword, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    change_pass_customer = crud.change_pass_customer(db, customer_id=customer_id, use_new=customer)

    return change_pass_customer


#### ITEMS


# get all items

@app_server.get("/items/", response_class=HTMLResponse, response_model=list[schemas.Item])
def read_items(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return templates.TemplateResponse("items.html", {"items": items, "request": request})

# get one item


@app_server.get("/items/{item_id}", response_class=HTMLResponse, response_model=schemas.Item)
def get_item(request: Request, item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    print(db_item.id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return templates.TemplateResponse("item.html", {"item": db_item, "request": request})


# put one item

@app_server.put("/items/{item_id}", response_model=schemas.ItemBase)
def update_item(item_id: int, item: schemas.ItemBase, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    updated_item = crud.update_item(db, item_id=item_id, item_new=item)
    return updated_item

# page 404


@app_server.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=exc.status_code)


@app_server.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=exc.status_code)
# end page 404

#####################################################################################################################################
# app_data (admin page)
app_data = FastAPI()
app_data.mount("/static", StaticFiles(directory="static"), name="static")
# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Main

# homepage
@app_data.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    print("page home")
    return templates.TemplateResponse("admin-home.html", {"request": request})

# sign-in
@app_data.get("/sign-in/", response_class=HTMLResponse)
async def sign_in(request: Request):
    return templates.TemplateResponse("admin-signin.html", {"request": request})

@app_data.post("/sign-in/", response_class=HTMLResponse)
def create_user(request: Request, user: schemas.UserCreate, db: Session = Depends(get_db)):
    print("done")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db=db, user=user)
    

    


# sign-up
@app_data.get("/sign-up/", response_class=HTMLResponse)
async def sign_in(request: Request):
    return templates.TemplateResponse("admin-signup.html", {"request": request})

# create nhiều Customers


@app_data.post("/Customers/", response_model=schemas.Customer)
def create_Customer(Customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_Customer = crud.get_customer_by_email(db, email=Customer.email)
    if db_Customer:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_customer(db=db, Customer=Customer)

# get all Customers


@app_data.get("/Customers/", response_model=list[schemas.Customer])
def read_Customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    Customers = crud.get_customers(db, skip=skip, limit=limit)
    return Customers

# get one Customer


@app_data.get("/Customers/{Customer_id}", response_model=schemas.Customer)
def read_Customer(Customer_id: int, db: Session = Depends(get_db)):
    db_Customer = crud.get_customer(db, Customer_id=Customer_id)
    if db_Customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_Customer

# put one Customer


@app_data.put("/Customers/{Customer_id}", response_model=schemas.Customer)
def update_Customer(Customer_id: int, Customer: schemas.Customer, db: Session = Depends(get_db)):
    db_Customer = crud.get_customer(db, Customer_id=Customer_id)
    if db_Customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    updated_Customer = crud.update_customer(db, Customer_id=Customer_id, Customer_new=Customer)
    return updated_Customer

# change pass Customer


@app_data.put("/Customers/{Customer_id}/change_pass", response_model=schemas.ChangePassword)
def change_pass(Customer_id: int, Customer: schemas.ChangePassword, db: Session = Depends(get_db)):
    db_Customer = crud.get_customer(db, Customer_id=Customer_id)
    if db_Customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    change_pass_Customer = crud.change_pass_customer(db, Customer_id=Customer_id, use_new=Customer)

    return change_pass_Customer

# create item for Customer


@app_data.post("/Customers/{Customer_id}/items/", response_model=schemas.Item)
def create_item_for_Customer(
    Customer_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_customer_item(db=db, item=item, Customer_id=Customer_id)

# get all items


@app_data.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

# get one item


@app_data.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id == item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# put one item


@app_data.put("/items/{item_id}", response_model=schemas.ItemBase)
def update_Customer(item_id: int, item: schemas.ItemBase, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    updated_item = crud.update_item(db, item_id=item_id, item_new=item)
    return updated_item

# page 404


@app_data.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=exc.status_code)


@app_data.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=exc.status_code)

# run uvicorn main:app1 --reload --port 8000////uvicorn main:app2 --reload --port 8080
