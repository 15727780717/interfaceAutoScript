# -*- coding: utf-8 -*-
# @Time    : 2025/4/10 11:02
# @Author  : Cqq
# @File    : assertion.py
# Description: 断言工具类
from jsonpath_ng import parse
from utils.logger import logger
from utils.database import DBConnection
import allure
import json


class Assertion:
    """断言工具类"""
    @staticmethod
    def assert_response(response, assertions):
        # 执行动态断言
        for assertion in assertions:
            for assert_type, (expr, expected) in assertion.items():
                # 获取实际值
                if expr == "status_code":
                    actual = response.status_code
                else:
                    try:
                        json_data = response.json()
                    except json.JSONDecodeError:
                        raise ValueError("响应不是有效的JSON格式")
                    # 从响应结果中匹配表达式
                    jsonpath_expr = parse(expr)
                    match_results = [match.value for match in jsonpath_expr.find(json_data)]
                    assert len(match_results) > 0, (
                        f"JSON表达式 '{expr}' 未匹配到数据,"
                        f"响应内容：{json.dumps(response, indent=2, ensure_ascii=False)}"
                    )
                    # 匹配实际结果值
                    actual = match_results[0]

                # 执行断言
                with allure.step(f"断言验证 {expr} {assert_type} {expected}"):
                    if assert_type == 'eq':
                        assert actual == expected, f"预期结果: {expected}, 实际结果: {actual}"
                    elif assert_type == 'contains':
                        assert expected in actual, f"预期结果包含: {expected}, 实际结果: {actual}"
                    # 统计记录断言结果到 Allure 报告中
                    allure.attach(
                        name="断言详情",
                        body=f"表达式: {expr}, 预期结果: {expected}, 实际结果: {actual}",
                        attachment_type=allure.attachment_type.TEXT
                    )

    @staticmethod
    def assert_database(sql, expected):
        """数据库记录断言"""
        db = DBConnection()
        actual = db.execute_query(sql)
        assert actual == expected, f"数据库校验失败：预期{expected}, 实际{actual}"
        logger.info("Database assertion passed")
