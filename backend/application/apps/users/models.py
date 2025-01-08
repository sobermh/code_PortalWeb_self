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

    class Meta:
        table = "user_info"
        description = "用户信息"

    def __repr__(self):
        return f"User (id={self.id}, username={self.username})"

    __str__ = __repr__


class UserLoginHistory(BaseModel):
    id = fields.IntField(description='主键', pk=True)
    # db_constraint=False 开启逻辑外键/虚拟外键，不使用数据库本身提供的物理外键，大表都强烈建议使用逻辑外键
    # on_delete=fields.OnDelete.NO_ACTION设置外键的级联操作，
    # NO_ACTION表示删除主键是不进行任何操作，
    # CASCADE表示删除主键时同时删除对应的外键，
    # RESTRICT表示删除外键前必须先删除所有对应的外键，
    # SET_NULL表示删除主键时，把对应外键的值全部改成NULL，
    # SET_DEFAULT表示删除主键时，把对应外键的值全部改成默认值
    user = fields.ForeignKeyField(description='用户', model_name='models.User', related_name='login_history_list',
                                  on_delete=fields.OnDelete.CASCADE, db_constraint=False)
    login_time = fields.DatetimeField(description='登陆时间', auto_now_add=True)

    class Meta:
        table = "user_login_history"
        description = "用户登陆历史"

    def __repr__(self):
        return (f"UserLoginHistory (id={self.id}, username={self.user.username}, "
                f"{self.login_time.strftime('%Y-%m-%d %H:%M:%S')})")

    __str__ = __repr__
