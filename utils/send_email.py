# -*- coding: utf-8 -*-
# @Time    : 2025/4/10 11:03
# @Author  : Cqq
# @File    : send_email.py
# Description: 发送邮件
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import zipfile
import tempfile
from config.settings import config
from utils.logger import logger

report_dir = config.REPORT_DIR


def zip_directory(directory_path, zip_path):
    """
    将目录压缩为 zip 文件
    :param directory_path: 目录路径
    :param zip_path:
    :return:
    """
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, directory_path)
                zipf.write(file_path, arcname)


def send_email():
    # 邮箱设置
    smtp_server = "smtp.qq.com"
    smtp_port = 465
    sender_email = config.SENDER_EMAIL  # 发件人邮箱
    sender_password = config.SENDER_PASSWORD  # 邮箱的授权码
    receiver_emails = config.RECEIVER_EMAILS  # 收件人邮箱

    # 创建临时zip文件
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp_file:
        zip_path = tmp_file.name

    try:
        # 压缩报告目录
        zip_directory(report_dir, zip_path)

        # 创建邮箱对象
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ", ".join(receiver_emails)  # 多个收件人用逗号分隔
        msg['Subject'] = '自动化测试报告'

        # 邮件正文
        body = """
        <html>
          <body>
            <p>本次自动化测试已完成，请查收附件中的 Allure 报告压缩包。</p>
            <p>解压后，请打开 index.html 文件查看完整报告。</p>
          </body>
        </html>
        """
        msg.attach(MIMEText(body, "html"))

        # 添加压缩文件作为附件
        with open(zip_path, "rb") as f:
            part = MIMEApplication(f.read(), Name="allure_report.zip")
            part["Content-Disposition"] = 'attachment; filename="allure_report.zip"'
            msg.attach(part)

        # 发送邮件
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_emails, msg.as_string())
        logger.info("邮件发送成功")

    except Exception as e:
        logger.error(f"邮件发送失败: {e}")
    finally:
        # 删除临时zip文件
        if os.path.exists(zip_path):
            os.remove(zip_path)


if __name__ == "__main__":
    send_email()
