from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user_info` MODIFY COLUMN `mobile` VARCHAR(16)   COMMENT '手机';
        ALTER TABLE `user_info` MODIFY COLUMN `email` VARCHAR(255)   COMMENT '邮箱';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user_info` MODIFY COLUMN `mobile` VARCHAR(16) NOT NULL  COMMENT '手机';
        ALTER TABLE `user_info` MODIFY COLUMN `email` VARCHAR(255) NOT NULL  COMMENT '邮箱';"""
