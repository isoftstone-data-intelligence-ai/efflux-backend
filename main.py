from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from exception.exception import global_exception_handlers
from controller import chat_controller, user_controller, login_controller, mcp_controller, chat_window_controller
import configparser
from core.security.middleware import AuthMiddleware

app = FastAPI(exception_handlers=global_exception_handlers)

# @app.middleware("http")
# async def middleware(request: Request, call_next):
#     response = await call_next(request)
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     response.headers["Access-Control-Allow-Headers"] = "*"
#     response.headers["Access-Control-Allow-Methods"] = "*"
#     return response

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，或者指定特定源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

# config
config_file = "config.ini"
config = configparser.ConfigParser()
config.read(config_file)
SECRET_KEY = config['SECURITY']['SECRET_KEY']
ALGORITHM = config['SECURITY']['ALGORITHM']
app.add_middleware(
    AuthMiddleware,
    secret_key=SECRET_KEY,
    algorithm=ALGORITHM,
    exclude_paths=["/auth/login", "/user/user", "/docs", "/openapi.json"]
)

app.include_router(chat_controller.router)
app.include_router(user_controller.router)
app.include_router(login_controller.router)
app.include_router(mcp_controller.router)
app.include_router(chat_window_controller.router)

# 在应用程序启动时初始化资源
# container = Container()

# 初始化数据库表
@app.on_event("startup")
async def init():
    print("init app")
    # await container.init_resources()

# @app.on_event("shutdown")
# async def shutdown_event():
    # await container.shutdown_resources()


@app.get("/")
async def root():
    return {"message": "Hello World"}