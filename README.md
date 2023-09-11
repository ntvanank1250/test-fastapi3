# test-fastapi3
test-fastapi2 + database domain

local ubuntu
# Ubuntu
///set up///
-create env:
    python3 -m venv test-fastapi 
- run env:
    source test-fastapi/bin/activate
- install requirements.txt:
    pip install -r requirements.txt
- copy file nginx-local.conf to /etc/nginx/nginx.conf
- copy file default-local to /etc/nginx/sites-enabled/default

/// run 2 server ///
    uvicorn main:app1 --reload --port 8000
    uvicorn main:app2 --reload --port 8080
    sudo service nginx restart