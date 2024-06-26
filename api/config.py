
import schemas
from utils import *


# Check session
def check_session(request, user_id):
    session = request.session
    if session.get("id") and user_id:
        if str(session["id"]) == str(user_id):
            return session["id"]
    return False


# Create user
def create_user(name, email, password):
    user = schemas.UserCreate
    user.name = name
    user.email = email
    user.password = password
    user.create_at = get_current_time()
    return user


# Create domain
def create_domain(name, user_id):
    domain = schemas.DomainCreate
    domain.name = name
    domain.status = 1
    domain.user_id = user_id
    domain.domain_id = create_domain_id_by_uuid4()
    domain.create_at = get_current_time()
    return domain


# Create origin
def create_origin(name, upstr_host, upstr_address, protocol, domain_id):
    origin = schemas.OriginCreate
    origin.name = name
    origin.upstr_host = upstr_host
    origin.upstr_address = upstr_address
    origin.protocol = protocol
    origin.domain_id = domain_id
    origin.create_at = get_current_time()
    return origin
