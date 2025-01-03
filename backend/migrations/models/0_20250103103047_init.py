from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `basemodel` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `updated_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `deleted_time` DATETIME(6)   COMMENT '删除时间'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user_info` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '主键',
    `created_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `updated_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `deleted_time` DATETIME(6)   COMMENT '删除时间',
    `username` VARCHAR(255) NOT NULL UNIQUE COMMENT '账号',
    `password` VARCHAR(255) NOT NULL  COMMENT '密码',
    `mobile` VARCHAR(16) NOT NULL UNIQUE COMMENT '手机',
    `email` VARCHAR(255) NOT NULL UNIQUE COMMENT '邮箱',
    `openid` VARCHAR(255)  UNIQUE COMMENT '微信OpenID',
    `nickname` VARCHAR(255)   COMMENT '昵称',
    `avatar` VARCHAR(500)   COMMENT '头像',
    `country` VARCHAR(255)   COMMENT '国家',
    `province` VARCHAR(255)   COMMENT '省份',
    `city` VARCHAR(255)   COMMENT '城市',
    `gender` INT   COMMENT '性别: 0-女, 1-男, 2-其他',
    `is_active` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 1,
    KEY `idx_user_info_mobile_299e81` (`mobile`),
    KEY `idx_user_info_email_210774` (`email`)
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
