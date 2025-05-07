# -*- coding: utf-8 -*-
# @Time    : 2025/4/10 11:02
# @Author  : Cqq
# @File    : database.py
# Description: 数据库操作类
import pymysql
from config.settings import config
from utils.logger import logger


class DBConnection:
    # 数据库操作工具类
    def __init__(self):
        self.connection = pymysql.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def __enter__(self):
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()

    def execute_query(self, sql):
        """执行查询语句"""
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            logger.debug(f"Executed SQL: {sql} => {len(result)} rows")
            return result
