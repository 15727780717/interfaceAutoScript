# -*- coding: utf-8 -*-
# @Time    : 2025/5/8 10:22
# @Author  : Cqq
# @File    : test_staking_scenario.py
# Description: STAKING 模块场景测试
import allure
import pytest
from utils.read_yaml import read_scenario_yaml
from utils.extract_parameters import extract_data
from utils.assertion import Assertion


@allure.feature("STAKING scenario test cases")
class TestStakingScenarioCases:
    cases = read_scenario_yaml("STAKING.yaml")

    @pytest.mark.parametrize("case", cases, ids=[case['name'] for case in cases])
    @allure.severity(allure.severity_level.CRITICAL)
    def test_case(self, case, api_client, auth_headers):
        with allure.step("测试用例名称: {}".format(case["name"])):
            # 处理请求参数
            request_data = case['request']
            # 发送请求
            with allure.step("发送请求"):
                try:
                    response = api_client.send_request(
                        method=request_data['method'],
                        url=request_data['url'],
                        headers=auth_headers,
                        data=request_data.get('data')
                    )
                    api_client.attach_request_response_details(response)
                except Exception as e:
                    allure.attach(str(e), name="请求异常")
                    raise

            # 判断 extract 是否在case中，如果在则匹配数据并存储到上下文管理器中
            if "extract" in case:
                extract_data(response, case['extract'])

            # 执行断言
            if "assertions" in case:
                with allure.step("响应断言"):
                    Assertion.assert_response(response, case['assertions'])

