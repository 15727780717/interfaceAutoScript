# -*- coding: utf-8 -*-
# @Time    : 2025/4/16 11:11
# @Author  : Cqq
# @File    : replace_dynamic_parameters.py
# Description: 替换动态参数
import re
from utils.custom_functions import *


class GlobalContext:
    params = {}  # 存储所有全局参数


# 白名单函数
ALLOWED_FUNCTIONS = {
    "get_eoa_sign": get_eoa_sign,
    "get_eoa_wallet": get_eoa_wallet,
    "get_timestamp": get_timestamp,
    "generate_redemption_code": generate_redemption_code
}


def replace_dynamic_values(text):
    """
    替换 text 中的 ${函数名()} 为实际值，若函数不存在则抛出 ValueError
    :param text: 字符串
    :return: 替换动态函数运行值后的字符串
    """
    PATTERN = r'\$\{([a-zA-Z_][a-zA-Z0-9_]*)\(\)\}'
    matches = re.findall(PATTERN, text)
    for func_name in matches:
        if func_name in ALLOWED_FUNCTIONS:
            # 获取函数返回值并强制转换为字符串
            func_value = str(ALLOWED_FUNCTIONS[func_name]())
            # 使用正则表达式进行准确替换
            text = re.sub(
                rf'\$\{{{func_name}\(\)}}',
                re.escape(func_value),  # 处理返回值中的特殊字符
                text)
        else:
            raise ValueError(f"函数未添加进白名单：{func_name}()")
    return text


def replace_global_params(text):
    """
    替换 text 中的 ${变量名} 为全局参数值，若参数不存在则抛出 KeyError
    :param text: 字符串
    :return: 替换全局变量参数值后的字符串
    """
    PATTERN = r'\$\{([a-zA-Z_][a-zA-Z0-9_]*)\}'
    matches = re.findall(PATTERN, text)
    for param_name in matches:
        if param_name in GlobalContext.params:
            # 将参数值强制转换为字符串
            param_value = str(GlobalContext.params[param_name])
            # 使用正则表达式进行准确替换
            text = re.sub(
                rf'\$\{{{param_name}}}',
                re.escape(param_value),  # 处理参数值中的特殊字符
                text
            )
        else:
            raise KeyError(f"全局变量key错误: {param_name}")
    return text


if __name__ == '__main__':
    test_url = '/api/v1/client/PaymentOrder/${orderId}'
    replace_dynamic_result = replace_dynamic_values(test_url)
    print(replace_dynamic_result)
    GlobalContext.params = {'orderId': 253}
    replace_global_result = replace_global_params(replace_dynamic_result)
    print(replace_global_result)
