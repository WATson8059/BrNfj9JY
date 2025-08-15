# 代码生成时间: 2025-08-15 18:53:32
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import base64
from cryptography.fernet import Fernet

# 密钥管理，应从环境变量或安全存储中加载
# 为了示例，这里使用一个硬编码的密钥
SECRET_KEY = 'your_very_secret_key_here'

# 初始化Fernet对象
cipher_suite = Fernet(SECRET_KEY)

class EncryptionDecryptionService:
    def __init__(self):
        self.cipher_suite = cipher_suite

    def encrypt(self, plaintext: str) -> str:
        """Encrypts the provided plaintext."""
        try:
            encrypted_text = self.cipher_suite.encrypt(plaintext.encode())
            return encrypted_text.decode()
        except Exception as e:
            raise ValueError(f"Encryption failed: {e}")

    def decrypt(self, encrypted_text: str) -> str:
        """Decrypts the provided encrypted text."""
        try:
            decrypted_text = self.cipher_suite.decrypt(encrypted_text.encode())
            return decrypted_text.decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")


@view_config(route_name='encrypt', request_method='POST', renderer='json')
def encrypt_view(request):
    """Endpoint for encrypting a password."""
    service = EncryptionDecryptionService()
    plaintext = request.json.get('password')
    if not plaintext:
        return Response(json_body={'error': 'Missing password in request'}, status=400)
    encrypted_text = service.encrypt(plaintext)
    return {'encrypted_password': encrypted_text}

@view_config(route_name='decrypt', request_method='POST', renderer='json')
def decrypt_view(request):
    """Endpoint for decrypting an encrypted password."""
    service = EncryptionDecryptionService()
    encrypted_text = request.json.get('encrypted_password')
    if not encrypted_text:
        return Response(json_body={'error': 'Missing encrypted password in request'}, status=400)
    decrypted_text = service.decrypt(encrypted_text)
    return {'decrypted_password': decrypted_text}

def main(global_config, **settings):
    """Main function for Pyramid application."""
    config = Configurator(settings=settings)
    config.add_route('encrypt', '/encrypt')
    config.add_route('decrypt', '/decrypt')
    config.scan()
    return config.make_wsgi_app()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main({})
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()