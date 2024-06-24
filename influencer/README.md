# Influencer Mgr Be

Social media (e.g. Tiktok) influencer management, backend.

# For test
need to add `"with_for_update": UnorderedCall,` to `UnifiedAlchemyMagicMock.unify` before execution


## 运行项目

```shell

# 建议 python 版本 3.10+
# 1.安装依赖
pip install -r requirements.txt
# 运行脚本 asgi.py
uvicorn main:app --reload
uvicorn asgi:app --host 0.0.0.0 --port 6006 --reload
nohup python3 -m uvicorn asgi:app --host 0.0.0.0 --port 6006 --workers=2 &
# http://127.0.0.1:6006/docs
# http://127.0.0.1:6006/redoc
```

## 相关文档
1. [starlette](https://www.starlette.io/#installation)
2. [FastAPI](https://fastapi.tiangolo.com/zh/)
3. ORM[Sqlalchemy](https://www.sqlalchemy.org/)
4. Redis 异步[aioredis](https://aioredis.readthedocs.io/)


## 目录结构参考
```
├─📂 FastAPI                       //服务端根目录（管理后台、接口）
│  ├─📂 app
│  │  ├─📂 home                    // 应用
│  │  │  ├─📂 router               // 应用 api 路由
│  │  │  ├─📂 schemas              // 入参校验数据，输出数据对象schemas
│  │  │  ├─📂 service              // service 数据处理层
│  │  │
│  │  ├─📂 config                  //配置文件
│  │  │  ├─📄 settings.py          //全站配置
│  │  │
│  │  ├─📂 core                    //核心依赖
│  │  │  ├─📄 events.py           //事件hooks
│  │  │  ├─📄 middlewares.py      //中间件
│  │  │  ├─📄 response.py         //返回方法封装
│  │  │
│  │  ├─📂 dependencies           // 核心依赖
│  │  │  ├─📄 databases.py        // 数据库 PostgreSQL
│  │  │  ├─📄 redis.py            // redis 未启用
│  │  │  ├─📄 jwt.py              // 用户鉴权
│  │  │
│  │  ├─📂 exceptions             // 全局异常
│  │  ├─📂 models                 // 实体模型
│  │  ├─📂 plugins                // 扩展插件
│  │  │  ├─📂 storage             //存储
│  │  │  │  ├─📄 storage_driver.py     //存储类
│  │  │
│  │  ├─📂 temporary              //运行时临时文件夹
│  │  ├─📂 utils                  //工具目录
│  │  │  ├─📄 utils.py            //工具方法
│  │  │
│  │  ├─📄 application.py         //项目入口文件
│  │
│  ├─📂 static              //静态目录
│  ├─📂 cli                 //快捷命令
│  ├─📂 tests               //测试用例（暂未使用）
│  │
│  ├─📄 .example.env        //项目环境配置示例
│  ├─📄 .env                //项目环境配置文件（最优化读取配置）
│  ├─📄 asgi.py             //项目运行入口
│  ├─📄 requirements.txt    //项目依赖文件
│  ├─📄 run_server.sh       //项目运行脚本
```
