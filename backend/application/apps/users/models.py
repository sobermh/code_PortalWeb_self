from tortoise import models, fields


class BaseModel(models.Model):
    created_time = fields.DatetimeField(description='创建时间', auto_now_add=True)
    updated_time = fields.DatetimeField(description="更新时间", auto_now=True)
    deleted_time = fields.DatetimeField(description="删除时间", null=True)

    class Meta:
        abstract = True


class User(BaseModel):
    id = fields.IntField(description='主键', pk=True)
    username = fields.CharField(description='账号', max_length=255, unique=True)
    password = fields.CharField(description='密码', max_length=255)
    mobile = fields.CharField(description='手机', max_length=16, index=True, unique=True)
    email = fields.CharField(description='邮箱', max_length=255, index=True, unique=True, null=True)

    openid = fields.CharField(description='微信OpenID', max_length=255, unique=True, null=True)
    nickname = fields.CharField(description='昵称', max_length=255, null=True)
    avatar = fields.CharField(description='头像', max_length=500, null=True)
    country = fields.CharField(description='国家', max_length=255, null=True)
    province = fields.CharField(description='省份', max_length=255, null=True)
    city = fields.CharField(description='城市', max_length=255, null=True)
    gender = fields.IntField(description='性别: 0-女, 1-男, 2-其他', null=True)
    remarks = fields.CharField(description="备注", max_length=255, null=True)
    is_deleted = fields.BooleanField(description="是否删除", default=False)

    # 元数据
    class Meta:
        table = "user_info"
        description = "用户信息"

    def __repr__(self):
        return f"User (id={self.id}, username={self.username})"

    __str__ = __repr__
