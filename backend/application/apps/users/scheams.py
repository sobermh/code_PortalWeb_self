import re
from typing import Any, Optional

from pydantic import BaseModel, field_validator, Field, EmailStr

from application.schemas import BaseResp


class UserRegisterReq(BaseModel):
    username: str = Field(..., description="用户名", min_length=4, max_length=20)
    password: str = Field(..., description="密码", min_length=6, max_length=20)
    mobile: Optional[str] = Field(None, description="手机号")
    email: Optional[str] = Field(None, description="邮箱")

    @field_validator('email')
    def validate_email(cls, v):
        if not v:
            return v
        email_regex = r"^(?![.-])[A-Za-z0-9._%+-]+(?:[A-Za-z0-9._%+-])*(?<=@)[A-Za-z0-9.-]+(?<=\.[A-Za-z]{2,})$"
        if not re.match(email_regex, v):
            raise ValueError('非法邮箱格式')
        return v


class UserLoginReq(BaseModel):
    username: str = Field(..., description='用户名', min_length=4, max_length=20)
    password: str = Field(..., description="密码", min_length=6, max_length=20)


class UserRegister(BaseModel):
    username: str = Field(..., description='用户名', min_length=4, max_length=20)


class UserRegisterResp(BaseResp):
    data: UserRegister = Field(..., description='用户信息')


class UserLogin(BaseModel):
    username: str = Field(..., description='用户名', min_length=4, max_length=20)


class UserLoginOutResp(BaseModel):
    data: UserLogin = Field(..., description='用户信息')
