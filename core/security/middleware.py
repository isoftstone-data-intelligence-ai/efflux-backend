# middleware.py
import contextvars
from fastapi import Request, HTTPException
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware

# 创建context variable
request_token_context = contextvars.ContextVar('request_token', default=None)


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, secret_key: str, algorithm: str, exclude_paths: list = None):
        super().__init__(app)
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.exclude_paths = exclude_paths if exclude_paths is not None else []

    async def dispatch(self, request: Request, call_next):
        # 检查请求路径是否在排除列表中
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)

        token = request.headers.get("Authorization")

        if token:
            try:
                # 去掉Bearer前缀
                token = token.split(" ")[1]
                # 解析token
                payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
                # 设置到context vars
                request_token_context.set(payload)
            except JWTError as e:
                raise HTTPException(status_code=401, detail="Invalid token")
        else:
            raise HTTPException(status_code=401, detail="Not authenticated")

        response = await call_next(request)
        return response