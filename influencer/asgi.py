# coding:utf-8

# from app.application import create_app
from log_config import LOGGING_CONFIG

# 容器运行入口
# app = create_app()

if __name__ == '__main__':
    import uvicorn

#    uvicorn.run(app, host='0.0.0.0', port=6006, log_config=LOGGING_CONFIG)

#     uvicorn.run(
#             app,
#             host='0.0.0.0',
#             port=6006,
#             reload=False,
#             workers=2,
#  #           root_path='',
#             log_config=LOGGING_CONFIG
#             )

    uvicorn.run(
        "app.application:create_app",
        host='0.0.0.0',
        port=6006,
        reload=False,
        workers=2,
        log_config=LOGGING_CONFIG
    )
