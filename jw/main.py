import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import router

STATIC_DIR = os.path.join(os.getcwd(), "static")
print(STATIC_DIR)

app = FastAPI()

# 跨域中间件
origins = [
    "http://101.35.200.235:8000",
    "http://localhost",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂在路由
app.include_router(router)

# 静泰文件
app.mount('/app/', StaticFiles(directory=STATIC_DIR), name='static')

# if __name__ == '__main__':
#     uvicorn.run(
#         'app',
#         host='0.0.0.0',
#         port=8080,
#         # reload=True,
#         # workers=1,
#         reload=True,
#         workers=1,
#         root_path=''
#     )
