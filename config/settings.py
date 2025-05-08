# -*- coding: utf-8 -*-
# @Time    : 2025/4/21 11:37
# @Author  : Cqq
# @File    : settings.py
# Description:
import os
from pathlib import Path

# 获取项目的基础目录
BASE_DIR = Path(__file__).parents[1]


class BaseConfig:
    # 基础配置：所有环境共享配置
    # 日志和报告目录
    LOG_DIR = BASE_DIR / "logs"
    # 测试报告目录
    REPORT_DIR = BASE_DIR / "report/allure_result"
    # 基础测试用例目录
    BASIC_DATA = BASE_DIR / "data/basic"
    # 场景测试用例目录
    SCENARIO_DATA = BASE_DIR / "data/scenario"

    # 登录钱包信息
    LOGIN_DATA = BASE_DIR / "data/login_data/eoa_wallet.yaml"
    EOA_WALLET_SIGN = "0x7739a5e0a93484a2e6ac974d3ca798506f2e392d28299e2def87a74cb3e1df211cb6b70ab21f7672a0c54b4a02371413056cf27fe51fce66c6deb58ed327df7e1c"
    EOA_WALLET_ADDRESS = "0x7da7b3c10fbd050fc9cb0d9df273d9f871ca621d"
    # 邮箱设置
    SENDER_EMAIL = "1659207757@qq.com"  # 发件人邮箱
    SENDER_PASSWORD = "kialjsucnbfcceei"  # 邮箱的授权码
    RECEIVER_EMAILS = ["1104434499@qq.com", "1659207757@qq.com"]  # 收件人邮箱

    # 数据库配置：可通过环境变量覆盖
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "test_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "test_db")


class DevConfig(BaseConfig):
    # 测试环境配置
    BASE_URL = "https://api.metaicon.minerhubs.link"


class StageConfig(BaseConfig):
    # 预发布环境
    BASE_URL = "https://admin.partypre.link"


class ProdConfig(BaseConfig):
    # 生产环境配置
    BASE_URL = "https://api.gamehubs.link"


def get_config():
    # 配置工厂函数，根据环境变量返回对应的配置类
    env = os.getenv("APP_ENV", "dev").lower()

    config_map = {
        "dev": DevConfig,
        "stage": StageConfig,
        "prod": ProdConfig
    }
    if env not in config_map:
        raise ValueError(f"Unknown environment: {env}")

    return config_map[env]()


# 实例化配置对象
config = get_config()
"""
设置环境变量（推荐）：
# Linux/Mac
export APP_ENV=stage

# Windows
set APP_ENV=prod
"""

if __name__ == '__main__':
    print(config.EOA_WALLET_ADDRESS)
    print(config.BASE_URL)
