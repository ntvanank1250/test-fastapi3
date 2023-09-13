# Create domain
@app_data.get("/users/{user_id}/domains/{domain_id}/create-origin",response_class=HTMLResponse)
async def create_origin(request: Request,user_id:int,domain_id:int):
    if request.session.get('id'):
        if request.session['id'] == user_id:
            return templates.TemplateResponse("admin-create-origins.html", {"user_id":user_id,"domain_id":domain_id,"request": request})

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
