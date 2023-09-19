import uuid
from datetime import datetime
from app import crud, models, schemas, database, redis_connecttion

#create domain_id
def create_domain_id_by_uuid4():
    uuid4 = str(uuid.uuid4())
    return uuid4


SessionLocal = database.SessionLocal
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get current time
def get_current_time():
    current_time = datetime.now()  # Lấy thời gian hiện tại
    # Chuyển đổi thành chuỗi string với định dạng ngày/tháng/năm
    formatted_time = current_time.strftime("%d/%m/%Y")
    return formatted_time