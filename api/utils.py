import uuid
from datetime import datetime
from api import database
from functools import wraps
from fastapi import status

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
    
def writelog(time_stamp, status_code='', link='', request_id='',message=''):
    if any(substring in message for substring in ['db', 'redis']):
        log_format = f'[{time_stamp}ms] - {message} ||  '
    else:
        log_format = f'[{time_stamp}ms] - {status_code} - {link} - {request_id}\n'
    log_file = open("api/logs/access.log", "a")
    log_file.write(log_format)
    log_file.close() 

def tracking_time_api(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        url = request.url
        request_id = str(uuid.uuid4())
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds() * 1000
        execution_time = round(execution_time, 4)
        writelog(time_stamp=execution_time,status_code=status.HTTP_200_OK,link=url,request_id=request_id)
        return result   
    return wrapper

def tracking_time_db(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds() * 1000
        execution_time = round(execution_time,5)
        message = 'for query from db'
        writelog(time_stamp=execution_time,message=message)
        return result
    return wrapper
