# FastAPI turtorial

## File Structure

├── app                  # "app" is a Python package
│   ├── __init__.py      # this file makes "app" a "Python package"
│   ├── main.py          # "main" module, e.g. import app.main
│   ├── dependencies.py  # "dependencies" module, e.g. import app.dependencies
│   ├── test_main.py     # the test file for main.py
│   └── routers          # "routers" is a "Python subpackage"
│   │   ├── __init__.py  # makes "routers" a "Python subpackage"
│   │   ├── items.py     # "items" submodule, e.g. import app.routers.items
│   │   └── users.py     # "users" submodule, e.g. import app.routers.users
│   └── internal         # "internal" is a "Python subpackage"
│       ├── __init__.py  # makes "internal" a "Python subpackage"
│       └── admin.py     # "admin" submodule, e.g. import app.internal.admin


## Environment
- environment: ~/python-virtual-environments/FastAPI
- run command: uvicorn main:app --reload

## The command uvicorn main:app refers to:

-    main: the file main.py (the Python "module").
-    app: the object created inside of main.py with the line app = FastAPI().
-    --reload: make the server restart after code changes. Only do this for development.


