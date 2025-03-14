from pydantic import BaseModel

class UserInit(BaseModel):
    name: str
    email: str
    password: str

class UserResult(BaseModel):
    id: int
    name: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
