# -*- coding: utf-8 -*-
# @Time    : 2024/9/10 11:02
# @Author  : Cqq
# @File    : logger.py
# Description: 记录日志
import logging
from datetime import datetime
from config.settings import config


def setup_logger():
    log_dir = config.LOG_DIR
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("api_test")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # 文件处理器
    log_file = log_dir / f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}_log.txt"
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


logger = setup_logger()
