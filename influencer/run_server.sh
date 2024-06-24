#!/usr/bin/env bash

# 运行服务 nohup uvicorn asgi:app --host 0.0.0.0 --port 6006 --reload &
# python3 -m uvicorn asgi:app --port 5000 --reload
# source venv/bin/activate
#uvicorn asgi:app --host 0.0.0.0 --port 6006 --reload # --reload causes 100% CPU?
# uvicorn asgi:app --host 0.0.0.0 --port 6006 --workers=4
/usr/local/bin/python3 asgi.py
# uvicorn asgi:app --host 0.0.0.0 --port 6006 --workers=2
