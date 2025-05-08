# -*- coding: utf-8 -*-
# @Time    : 2025/4/10 10:57
# @Author  : Cqq
# @File    : conftest.py
# Description:
import pytest
from utils.request_handler import RequestHandler
from utils.read_yaml import read_login_data
from utils.replace_dynamic_parameters import GlobalContext
import os
from utils.assertion import Assertion
from config.settings import config


@pytest.fixture(scope="session")
def api_client():
    client = RequestHandler()
    yield client
    GlobalContext.params.clear()


@pytest.fixture(scope='session')
def login_request_data():
    # 获取登录接口的请求数据
    login_entry = read_login_data()[0]
    return login_entry['request']


@pytest.fixture(scope='session')
def auth_headers(login_request_data):
    request_method = login_request_data['method']
    request_url = login_request_data['url']
    request_headers = login_request_data.get('headers', {})
    request_data = login_request_data.get('data')

    # 发送登录请求
    request_handler = RequestHandler()
    res = request_handler.send_request(method=request_method, url=request_url, data=request_data,
                                       headers=request_headers)
    # 执行断言
    Assertion.assert_response(res, read_login_data()[0]['assertions'])
    # 提取token并构造headers
    res_token = res.json()['result']['token']
    # 拼接headers传递给后续接口
    auth_headers = {"Token": res_token, "Content-Type": "application/json"}
    return auth_headers


# 配置 Allure 报告中的 Environment
def pytest_sessionstart(session):
    allure_dir = config.REPORT_DIR
    os.makedirs(allure_dir, exist_ok=True)
    with open(f"{allure_dir}/environment.properties", "w") as f:
        f.write(f"BaseURL={config.BASE_URL}\n")
        f.write("TestingEnvironment=FZ\n")
        f.write("PythonVersion=3.8\n")


# 强制解码 Allure 报告中的名称
def pytest_collection_modifyitems(items):
    for item in items:
        item.name = item.name.encode("utf-8").decode("utf-8")
        item._nodeid = item.nodeid.encode("utf-8").decode("utf-8")

