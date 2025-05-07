# -*- coding: utf-8 -*-
# @Time    : 2025/4/10 14:00
# @Author  : Cqq
# @File    : request_handler.py
# Description: 请求类
import requests
from config.settings import config
from utils.logger import logger
from utils.replace_dynamic_parameters import replace_dynamic_values, replace_global_params
from urllib.parse import urljoin
import time
import allure


class RequestHandler:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = config.BASE_URL

    # 处理动态参数并发送请求
    def send_request(self, method, url, data=None, **kwargs):
        try:
            # 1.替换url中的动态函数
            url = replace_dynamic_values(url)
            # 2.替换url中的全局参数
            url = replace_global_params(url)
            # 3.拼接url
            full_url = urljoin(self.base_url, url)

            # 处理请求数据
            request_data = data
            if isinstance(data, dict):
                request_data = {}
                for key, value in data.items():
                    # 仅当值为字符串类型时才执行替换，保持原数据类型
                    if isinstance(value, str):
                        processed = replace_dynamic_values(value)
                        processed = replace_global_params(processed)
                        request_data[key] = processed
                    else:
                        request_data[key] = value

            # 记录请求日志
            logger.info(f"Request: {method} {full_url}")
            logger.debug(f"Request Data: {request_data}")
            logger.debug(f"Request Headers: {self.session.headers}")
            # 发送请求开始时间
            start_time = time.perf_counter()
            # 发送请求
            response = self.session.request(method=method, url=full_url, json=request_data, timeout=5, **kwargs)
            # 计算响应时间(秒)
            elapsed = time.perf_counter() - start_time
            with allure.step("接口性能监控"):
                allure.attach(
                    f"Response time: {elapsed:.3f}s",
                    name="接口响应时间",
                    attachment_type=allure.attachment_type.TEXT
                )

            # 记录响应日志
            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response time: {elapsed:.3f}s")
            logger.debug(f"Response body: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

    @staticmethod
    def attach_request_response_details(response):
        """
        记录请求和响应到 Allure 报告中
        :param response: 接口响应
        :return:
        """
        allure.attach(response.request.url, name="请求URL", attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.request.method, name="请求方法", attachment_type=allure.attachment_type.TEXT)
        if response.request.body:
            allure.attach(str(response.request.body), name="请求体", attachment_type=allure.attachment_type.TEXT)
        allure.attach(str(response.status_code), name="状态码", attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, name="响应体", attachment_type=allure.attachment_type.TEXT)
