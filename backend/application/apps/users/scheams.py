import re
from typing import Any, Optional

from pydantic import BaseModel, field_validator, Field, EmailStr, model_validator

from application.apps.users.utils import Hashing
from application.schemas import BaseResp


class UserRegisterReq(BaseModel):
    username: str = Field(..., description="用户名", min_length=4, max_length=20)
    password: str = Field(..., description="密码", min_length=6, max_length=20)
    mobile: str = Field(..., description="手机号")
    sms_code: str = Field(..., description="短信验证码")
    email: Optional[str] = Field(None, description="邮箱")

    @field_validator('email')
    def validate_email(cls, v):
        if not v:
            return v
        email_regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if not re.match(email_regex, v):
            raise ValueError('非法邮箱格式')
        return v

    @field_validator('mobile')
    def validate_mobile(cls, v):
        if not v:
            return v
        mobile_regex = r"^1[3-9]\d{9}$"
        if not re.match(mobile_regex, v):
            raise ValueError('非法手机号格式')
        return v

    @model_validator(mode='after')
    def model_validator(self):
        hashing = Hashing()
        self.password = hashing.hash(self.password)

        return self


class UserLoginReq(BaseModel):
    username: str = Field(..., description='用户名', min_length=4, max_length=20)
    password: str = Field(..., description="密码", min_length=6, max_length=20)


class UserRegister(BaseModel):
    username: str = Field(..., description='用户名', min_length=4, max_length=20)


class UserRegisterResp(BaseResp):
    data: Optional[UserRegister] = Field(..., description='用户信息')


class UserLogin(BaseModel):
    username: str = Field(..., description='用户名', min_length=4, max_length=20)


class UserLoginOutResp(BaseModel):
    data: Optional[UserLogin] = Field(..., description='用户信息')
