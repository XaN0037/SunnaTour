from rest_framework.authentication import TokenAuthentication
import base64

class BearerAuth(TokenAuthentication):
    keyword = 'Bearer'


def code_decoder(code, decode=False):
    if decode:
        return base64.b64decode(code).decode()
    else:
        return base64.b64encode(f"{code}".encode("utf-8")).decode()


