from datetime import datetime, timezone, timedelta
from asyncpg.pgproto.pgproto import timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from core.common.logger import get_logger
from core.common.container import Container
from dto.user_dto import Token
from service.user_service import UserService
from passlib.context import CryptContext
import configparser
import jwt

router = APIRouter(prefix="/auth", tags=["Authentication"])
# 显示创建日志
logger = get_logger(__name__)

# config
config_file = "config.ini"
config = configparser.ConfigParser()
config.read(config_file)
# security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = config['SECURITY']['SECRET_KEY']
ALGORITHM = config['SECURITY']['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = config['SECURITY']['ACCESS_TOKEN_EXPIRE_MINUTES']


# 从容器中获取注册在容器中的user Service
def get_user_service() -> UserService:
    us = Container.user_service()  #
    return us


# 密码校验
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 密码hash
def get_password_hash(password):
    return pwd_context.hash(password)


# 验证用户
async def authenticate_user(username: str,
                            password: str,
                            user_service: UserService = Depends(get_user_service)):
    user = await user_service.get_user_by_name(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


# 创建令牌
async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 登录成功，颁发令牌
async def login_for_access_token(username: str, password: str) -> Token:
    user = await authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = await create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


# 登录接口
@router.post("/login", summary="登录")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    return await login_for_access_token(form_data.username, form_data.password)


# 登出接口 需要token
@router.post("/logout", summary="登出")
async def get_current_user(token: str = Depends(oauth2_scheme), user_service: UserService = Depends(get_user_service)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception
    user = await user_service.get_user_by_name(username)
    if user is None:
        raise credentials_exception
    return user

@router.post("/logout", summary="登出")
async def logout(current_user = Depends(get_current_user)):
    # 由于使用了JWT，服务器端不需要存储token状态
    # 客户端只需要删除本地存储的token即可
    # 这里可以添加一些额外的清理工作，比如记录日志等
    logger.info(f"User {current_user.name} logged out")
    return {"message": "Logged out successfully"}
