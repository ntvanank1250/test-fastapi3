from fastapi import Depends, FastAPI, HTTPException, Request, Form, Cookie
from sqlalchemy.orm import Session
from app import crud, models, schemas, database, redis_connecttion
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime
import uuid
import redis

def generate_domain_id():
    domain_id = str(uuid.uuid4())
    return domain_id

templates = Jinja2Templates(directory="templates")

SessionLocal = database.SessionLocal
engine = database.engine

models.Base.metadata.create_all(bind=engine)


# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


###### CUSTOMER + ITEM

app_server = FastAPI()

# Đường dẫn tới thư mục chứa các tệp tĩnh
app_server.mount("/static", StaticFiles(directory="static"), name="static")


# homepage
@app_server.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


#Customers

# get customers
@app_server.get("/customers/", response_class=HTMLResponse, response_model=list[schemas.Customer])
def read_customers(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db) ):
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


# ITEM


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

#####################################################################################################################################
### USER + DOMAIN + ORIGIN


app_data = FastAPI()

# Khai báo các cấu hình cho session

# Đường dẫn tới thư mục chứa các tệp tĩnh
app_data.mount("/static", StaticFiles(directory="static"), name="static")
app_data.add_middleware(SessionMiddleware, secret_key="some-random-string")

# Homepage
@app_data.get("/", response_class=HTMLResponse)
async def homepage(request: Request,db: Session = Depends(get_db)):
    # origin = crud.get_origin(db=db, origin_id=1)
    # print(origin.domain.name)
    # key = str(origin.domain.name)
    # value = str(origin.protocol) + '|' + str(origin.upstr_host) + '|' + str(origin.upstr_address)
    # r = redis_connecttion.get_redis_connection()
    # r.set(key, value)
    return templates.TemplateResponse("admin-home.html", {"request": request})

# Logout
@app_data.get("/logout")
def logout(request: Request):
    session = request.session
    session.clear()  # Xóa toàn bộ thông tin phiên người dùng
    return templates.TemplateResponse("admin-home.html", {"request": request})
# USER

# sign-in
@app_data.get("/sign-in", response_class=HTMLResponse)
async def sign_in(request: Request):
    if  request.session.get('id'):
        return RedirectResponse(url=f"/users/{request.session['id']}/domains", status_code=302)
    return templates.TemplateResponse("admin-signin.html", {"request": request})

@app_data.post("/sign-in", response_class=HTMLResponse)
async def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    print("dang sign in")
    print("email: " + email)
    print("password: " + password)
    db_user = crud.get_user_by_email(db, email=email)
    if db_user:
        if db_user.password == password:
            session = request.session
            session["username"] = db_user.name
            session["email"] = db_user.name
            session["id"] = db_user.id
            return RedirectResponse(url=f"/users/{db_user.id}/domains", status_code=302)
        return templates.TemplateResponse("admin-signin.html", {"message_pass":"Sai password", "request": request})
    return templates.TemplateResponse("admin-signin.html", {"message_email":"Email không tồn tại", "request": request})


# sign-up
@app_data.get("/sign-up", response_class=HTMLResponse)
async def sign_up(request: Request):
    return templates.TemplateResponse("admin-signup.html", {"request": request})

@app_data.post("/sign-up", response_class=HTMLResponse)
async def sign_up(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...),repassword: str = Form(...), db: Session = Depends(get_db)):
    print("dang sign up")
    check_email = crud.get_user_by_email(db, email=email)
    if check_email :
        return templates.TemplateResponse("admin-signup.html", {"message_email":"Email đã tồn tại", "request": request})
    if password != repassword:
        return templates.TemplateResponse("admin-signup.html", {"message_pass":"Pass có giống nhau dell đâu mà tạo được tài khoản", "request": request})
    user = schemas.UserCreate
    current_time = datetime.now()# Lấy thời gian hiện tại
    formatted_time = current_time.strftime("%d/%m/%Y") # Chuyển đổi thành chuỗi string với định dạng ngày/tháng/năm
    print(formatted_time) # In thời gian đã định dạng
    user.name = name
    user.email = email
    user.password = password
    user.create_at = formatted_time
    crud.create_user(db=db, user=user )
    return templates.TemplateResponse("admin-signin.html",{"request": request})

# Domains

@app_data.get("/users/{user_id}/domains",response_model=list[schemas.DomainCreate])
def get_domains(request: Request,user_id:int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if request.session.get('id'):
        if request.session['id'] == user_id:
            print("dang lay domain")
            user_id = user_id
            domains = crud.get_domains(db,user_id=user_id, skip=skip, limit=limit)
            if domains:
                request.session['domain_ids'] = list()
                for domain in domains:
                    request.session['domain_ids'].append(domain.id)
                print (request.session['domain_ids'])
                return templates.TemplateResponse("admin-domain.html", {"domains": domains,"user":request.session['username'],"user_id":user_id, "request": request})
            else:
                return templates.TemplateResponse("admin-domain.html", {"domains": domains,"user":request.session['username'],"user_id":user_id, "request": request})
        return templates.TemplateResponse("admin-domain.html", {"domains": [],"user":request.session['username'],"user_id":user_id,"message":"Dell phải domains của bạn", "request": request})
    return RedirectResponse(url="/sign-in", status_code=302)

# Create domain
@app_data.get("/users/{user_id}/create-domain",response_class=HTMLResponse)
async def create_domain(request: Request,user_id:int):
    if request.session.get('id'):
        if request.session['id'] == user_id:
            return templates.TemplateResponse("admin-create-domain.html", {"user_id":user_id,"request": request})

    return templates.TemplateResponse("admin-domain.html", {"domains": [],"message":"Dell phải domains của bạn","user_id":user_id, "request": request})

@app_data.post("/users/{user_id}/create-domain",response_model=schemas.DomainCreate)
def create_domain(request: Request,user_id:int, name: str = Form(...), db: Session = Depends(get_db)):
    domain = schemas.DomainCreate
    current_time = datetime.now()# Lấy thời gian hiện tại
    formatted_time = current_time.strftime("%d/%m/%Y") # Chuyển đổi thành chuỗi string với định dạng ngày/tháng/năm
    domain_id = generate_domain_id()
    domain.name = name
    domain.status = 1
    domain.user_id = user_id
    domain.domain_id = domain_id
    domain.create_at = formatted_time
    crud.create_domain(db=db, domain=domain )
    return RedirectResponse(url=f"/users/{user_id}/domains", status_code=302)

# Origins
@app_data.get("/users/{user_id}/domains/{domain_id}/origins",response_model=list[schemas.OriginCreate])
def get_domains(request: Request,user_id:int, domain_id:int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if request.session.get('id'):
        if request.session['id'] == user_id:
            origins = crud.get_origins(db, domain_id=domain_id, skip=skip, limit=limit)
            if origins:
                request.session['origin_ids'] = list()
                for origin in origins:
                    request.session['origin_ids'].append(origin.id)
                return templates.TemplateResponse("admin-origin.html", {"origins": origins,"user":request.session['username'],"user_id":user_id,"domain_id":domain_id, "request": request})
            else:
                return templates.TemplateResponse("admin-origin.html", {"origins": origins,"user":request.session['username'],"user_id":user_id,"domain_id":domain_id,"message":"Dell có origins", "request": request})
        return templates.TemplateResponse("admin-domain.html", {"origins": [],"user":request.session['username'],"user_id":user_id,"domain_id":domain_id,"message":"Dell phải origins của bạn", "request": request})
    return RedirectResponse(url="/sign-in", status_code=302)


@app_data.get("/users/{user_id}/domains/{domain_id}/origins/{origin_id}",response_model=list[schemas.OriginCreate])
async def get_data_origin(request: Request,user_id:int, domain_id:int,origin_id:int, db: Session = Depends(get_db)):
    print("dang lay data")
    origin = crud.get_origin(db=db, origin_id=origin_id)
    print(f"origin id: {origin.id}")

    print(origin.domain.name)
    key = str(origin.domain.name)
    value = str(origin.protocol) + '|' + str(origin.upstr_host) + '|' + str(origin.upstr_address)
    r = redis_connecttion.get_redis_connection()
    r.flushall()
    r.set(key, value)
    return RedirectResponse(f"/users/{user_id}/domains/{domain_id}/origins",status_code=302)
# Create domain
@app_data.get("/users/{user_id}/domains/{domain_id}/create-origin",response_class=HTMLResponse)
async def create_origin(request: Request,user_id:int,domain_id:int):
    if request.session.get('id'):
        if request.session['id'] == user_id:
            return templates.TemplateResponse("admin-create-origin.html", {"user_id":user_id,"domain_id":domain_id,"request": request})

    return templates.TemplateResponse("admin-domain.html", {"domains": [],"message":"Dell phải domains của bạn","user_id":user_id, "request": request})

@app_data.post("/users/{user_id}/domains/{domain_id}/create-origin",response_model=schemas.OriginCreate)
def create_origin(request: Request,user_id:int,domain_id:int, name: str = Form(...),upstr_host: str = Form(...),upstr_address: str = Form(...),protocol: str = Form(...), db: Session = Depends(get_db)):
    origin = schemas.OriginCreate
    current_time = datetime.now()# Lấy thời gian hiện tại
    formatted_time = current_time.strftime("%d/%m/%Y") # Chuyển đổi thành chuỗi string với định dạng ngày/tháng/năm
    print(formatted_time) # In thời gian đã định dạng
    origin.name = name
    origin.upstr_host = upstr_host
    origin.upstr_address = upstr_address
    origin.protocol = protocol
    origin.domain_id = domain_id
    origin.create_at = formatted_time
    crud.create_origin(db=db, origin=origin )
    return RedirectResponse(url=f"/users/{user_id}/domains/{domain_id}/origins", status_code=302)

# page 404
@app_data.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=exc.status_code)


@app_data.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=exc.status_code)

#  uvicorn main:app_server --reload --port 8000////uvicorn main:app_data --reload --port 8080
