<!-- # test-fastapi3 -->
test-fastapi2 + database domain

local ubuntu
<!-- # Ubuntu -->
///set up///
-create env:
    python3 -m venv test-fastapi 
- run env:
    source test-fastapi/bin/activate
- install requirements.txt:
    pip install -r requirements.txt
- copy file nginx-local.conf to /etc/nginx/nginx.conf
- copy file default-local to /etc/nginx/sites-enabled/default

/// run server ///
uvicorn main:app --reload --port 8080