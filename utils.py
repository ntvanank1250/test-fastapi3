import uuid
from datetime import datetime
from app import database

SessionLocal = database.SessionLocal


def create_domain_id_by_uuid4():
    uuid4 = str(uuid.uuid4())
    return uuid4
# Create domain id


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Get db


def get_current_time():
    current_time = datetime.now()
    # Convert time to string format day/month/year
    formatted_time = current_time.strftime("%d/%m/%Y")
    return formatted_time
# Get current time


def to_int(value):
    if not value:
        return 0
    try:
        value = int(float(value))
        return value
    except Exception:
        return 0
