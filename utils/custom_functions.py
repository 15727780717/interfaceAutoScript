# -*- coding: utf-8 -*-
# @Time    : 2025/4/11 17:16
# @Author  : Cqq
# @File    : custom_functions.py
# Description: 自定义函数库
import time
import random
import string
from config.settings import config


# 生成毫秒级时间戳
def get_timestamp():
    return int(time.time() * 1000)


# 生成 1-100 之间的随机整数
def get_randomInt():
    return random.randint(0, 100)


# 生成6位的随机字符串
def generate_random_string():
    letters = string.ascii_letters  # 包含所有字母的字符串
    random_string = ''.join(random.choice(letters) for _ in range(6))
    return random_string


# 获取EOA钱包签名信息
def get_eoa_sign():
    return config.EOA_WALLET_SIGN


# 获取EOA钱包地址
def get_eoa_wallet():
    return config.EOA_WALLET_ADDRESS


# 生成俱乐部兑换码
def generate_redemption_code():
    """生成8位数字+大写字母的兑换码"""
    # 定义字符池：数字(0-9) + 大写字母(A-Z)
    characters = string.digits + string.ascii_uppercase
    # 随机选择8个字符并组合成字符串
    code = ''.join(random.choice(characters) for _ in range(8))
    return code


if __name__ == '__main__':
    print(generate_redemption_code())
