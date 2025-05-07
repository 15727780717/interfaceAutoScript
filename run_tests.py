# -*- coding: utf-8 -*-
# @Time    : 2025/4/16 20:51
# @Author  : Cqq
# @File    : run_tests.py
# Description: 框架运行主入口
import pytest
import os


def run_tests():
    # 清理历史报告
    if os.path.exists("./report"):
        os.system("rmdir /s /q report")

    # 执行 pytest 测试
    pytest.main()

    # 生成 Allure 报告
    os.system("allure generate ./report/allure_result -o ./report/html --clean")

    # 自动打开报告
    os.system("allure open ./report/html")


if __name__ == '__main__':
    run_tests()


