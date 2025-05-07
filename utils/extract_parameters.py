# -*- coding: utf-8 -*-
# @Time    : 2025/4/10 14:01
# @Author  : Cqq
# @File    : extract_parameters.py
# Description: 提取依赖数据，从接口的响应数据中查找表达式匹配值并存入上下文管理器
from jsonpath_ng import parse
from utils.replace_dynamic_parameters import GlobalContext
from utils.logger import logger
import allure


def extract_data(response, extract_rules):
    """
    在响应数据中查找匹配的值并存入上下文
    :param response: 响应数据
    :param extract_rules: YAML文件中的 extract 配置，列表类型
    :return:
    """
    if isinstance(extract_rules, list):
        # 遍历匹配规则
        for extract in extract_rules:
            for key, expr in extract.items():
                # 将字符串形式的JSONPath表达式解析为可执行对象
                jsonpath_expr = parse(expr)
                # 执行查询，结果存储在 matches 列表中
                matches = jsonpath_expr.find(response.json())
                if not matches:
                    raise ValueError(f"No expression matched: {expr}")
                # 将提取结果存入上下文管理器
                GlobalContext.params[key] = matches[0].value
                with allure.step("提取数据"):
                    allure.attach(
                        f"match to extract value: {matches[0].value}",
                        name="表达式提取数据",
                        attachment_type=allure.attachment_type.TEXT
                    )
                logger.info(f"Match to extract value：{matches[0].value}")
    else:
        logger.error(f"extract_rules {extract_rules} not list type")
        raise


if __name__ == '__main__':
    from utils.request_handler import RequestHandler
    from utils.read_yaml import read_cases_data

    data = read_cases_data()
    test_request = RequestHandler()
    test_headers = {"Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiMHg3ZGE3YjNjMTBmYmQwNTBmYzljYjBkOWRmMjczZDlmODcxY2E2MjFkaWY3YjVlM2hxM3FyIiwibG9naW5UeXBlIjo3LCJpYXQiOjE3NDQ5NDQwMTUsImV4cCI6MTc0NDk4NzIxNX0.MeuIXDwznhye1DMhH4ai08bSWxMQDuBaYfyE0T4f7EY", "content-type": "application/json"}
    url = "https://api.metaicon.minerhubs.link/api/v1/client/PaymentOrder"
    test_data = {"paymentType": 1, "currencyId": 7, "goodIds": "27", "goodNum": "1"}
    res = test_request.send_request(method="POST", url=url, headers=test_headers, data=test_data)
    print(res.json())

    # test_extract_rules = [{'orderId': '$.result'}]
    test_extract_rules = data[0]['extract']
    extract_data(res, test_extract_rules)
    print(GlobalContext.params)

