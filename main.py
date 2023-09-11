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

### app1
app1 = FastAPI()

# Đường dẫn tới thư mục chứa các tệp tĩnh
app1.mount("/static", StaticFiles(directory="static"), name="static")



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# homepage
@app1.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
# end homepage

# page_all_users
@app1.get("/users/", response_class=HTMLResponse, response_model=list[schemas.User])
def read_users(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), ):
    users = crud.get_users(db, skip=skip, limit=limit)
    print (users)
    return templates.TemplateResponse("users.html", {"users": users, "request": request})
# end page_all_users

# create  users
@app1.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return crud.create_user(db=db, user=user)




# get one user
@app1.get("/users/{user_id}", response_class=HTMLResponse, response_model=schemas.User)
def read_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user.html", {"user": db_user, "request": request})

# put one user
@app1.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = crud.update_user(db, user_id=user_id, user_new=user)
    return updated_user

# change pass user
@app1.put("/users/{user_id}/change_pass", response_model=schemas.ChangePassword)
def change_pass(user_id: int, user: schemas.ChangePassword, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    change_pass_user = crud.change_pass_user(db, user_id=user_id, use_new=user)
    
    return change_pass_user

#create item for user
@app1.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

# get all items
@app1.get("/items/", response_class=HTMLResponse, response_model=list[schemas.Item])
def read_items(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return templates.TemplateResponse("items.html", {"items": items, "request": request})

# get one item
@app1.get("/items/{item_id}",response_class=HTMLResponse, response_model=schemas.Item)
def get_item(request: Request, item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    print (db_item.id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return templates.TemplateResponse("item.html", {"item": db_item, "request": request})

# put one item
@app1.put("/items/{item_id}", response_model=schemas.ItemBase)
def update_user(item_id: int, item: schemas.ItemBase, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    updated_item = crud.update_item(db, item_id=item_id, item_new=item)
    return updated_item

### app2
app2 = FastAPI()


# Main
@app2.get("/")
async def root():
    return {"message": "Hello from FastAPI on port 8080"}

# create nhiều users
@app2.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return crud.create_user(db=db, user=user)

# get all users
@app2.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# get one user
@app2.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# put one user
@app2.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = crud.update_user(db, user_id=user_id, user_new=user)
    return updated_user

# change pass user
@app2.put("/users/{user_id}/change_pass", response_model=schemas.ChangePassword)
def change_pass(user_id: int, user: schemas.ChangePassword, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    change_pass_user = crud.change_pass_user(db, user_id=user_id, use_new=user)
    
    return change_pass_user

#create item for user
@app2.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

# get all items
@app2.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

# get one item
@app2.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id==item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# put one item
@app2.put("/items/{item_id}", response_model=schemas.ItemBase)
def update_user(item_id: int, item: schemas.ItemBase, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    updated_item = crud.update_item(db, item_id=item_id, item_new=item)
    return updated_item

# if __name__ == "__main__":
#     uvicorn.run(app1, host="127.0.0.1", port=8000)
#     uvicorn.run(app2, host="127.0.0.1", port=8080)

#### run uvicorn main:app1 --reload --port 8000////uvicorn main:app2 --reload --port 8080

# page 404
@app1.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=exc.status_code)


@app1.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=exc.status_code)
# end page 404