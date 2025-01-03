from typing import Optional, Any

from pydantic import BaseModel, Field


class BaseResp(BaseModel):
    code: int = Field(..., description='状态码')
    msg: str = Field(..., description='状态信息')
    data: Optional[Any] = Field(None, description='返回数据')