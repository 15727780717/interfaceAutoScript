# -*- coding: utf-8 -*-
# @Time    : 2025/4/11 10:28
# @Author  : Cqq
# @File    : read_yaml.py
# Description: 读取 yaml 文件数据
import itertools
import yaml
from config.settings import config
from utils.logger import logger
from pathlib import Path


def read_login_data():
    """
    读取登录数据
    :return: 以列表形式返回登录数据
    """
    # 登录信息路径
    data_file = config.LOGIN_DATA
    with open(data_file, encoding='utf-8') as file:
        data = yaml.safe_load(file)
        return data


def read_cases_data():
    """
    读取 /data/cases_data 目录下所有的 yaml 文件数据
    :return: 列表形式返回 yaml 文件数据
    """
    if not config.SCENARIO_DATA.exists():
        raise FileNotFoundError(f"Test file directory {config.SCENARIO_DATA} does not exist!")
    # 创建空列表用于存储所有结果
    result_list = []
    try:
        for f in config.SCENARIO_DATA.glob("*.yaml"):
            with open(f, encoding="utf-8", errors="ignore") as file:
                data = yaml.safe_load(file)
                result_list.append(data)  # 将每个文件的结果追加到列表
        # 展开嵌套列表，将全部数据装填成[{}]
        flattened_data = list(itertools.chain(*result_list))
        return flattened_data  # 返回包含所有结果的列表
    except UnicodeError:
        logger.error("YAML file encoding error")


def read_basic_yaml(file_name):
    if not config.BASIC_DATA.exists():
        raise FileNotFoundError(f"Test file directory {config.BASIC_DATA} does not exist!")
    try:
        file_path = Path.joinpath(config.BASIC_DATA, file_name)
        with open(file_path, encoding='utf-8', errors='ignore') as f:
            data = yaml.safe_load(f)
            return data
    except UnicodeError:
        logger.error("YAML file encoding error")


def read_scenario_yaml(file_name):
    if not config.SCENARIO_DATA.exists():
        raise FileNotFoundError(f"Test file directory {config.SCENARIO_DATA} does not exist!")
    try:
        file_path = Path.joinpath(config.SCENARIO_DATA, file_name)
        with open(file_path, encoding='utf-8', errors='ignore') as f:
            data = yaml.safe_load(f)
            return data
    except UnicodeError:
        logger.error("YAML file encoding error")


if __name__ == '__main__':
    res = read_scenario_yaml("STORE.yaml")
    print(res)






