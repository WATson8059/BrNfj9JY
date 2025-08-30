# 代码生成时间: 2025-08-30 21:34:29
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
import os
import base64
from cryptography.fernet import Fernet

# 密码加密解密工具类
class PasswordCryptTool:
    def __init__(self, key):
        """初始化加密工具，生成密钥"""
        self.key = key
        self.cipher_suite = Fernet(self.key)

    def encrypt(self, password):
        """加密密码"""
        try:
            return self.cipher_suite.encrypt(password.encode()).decode()
        except Exception as e:
            raise Exception(f"加密失败：{str(e)}")

    def decrypt(self, encrypted_password):
        """解密密码"""
        try:
            return self.cipher_suite.decrypt(encrypted_password.encode()).decode()
        except Exception as e:
            raise Exception(f"解密失败：{str(e)}")

# Pyramid视图函数
@view_config(route_name='encrypt', renderer='json')
def encrypt_view(request):
    "