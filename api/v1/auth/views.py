import random

from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.v1.auth.serializer import Userserializer
from api.models import User, OTP
import string
import uuid

from api.v1.auth.service import sms_sender
from base.helper import code_decoder


class AuthView(GenericAPIView):
    serializer_class = Userserializer

    def post(self, request, *args, **kwargs):
        data = request.data
        method = data.get('method')
        params = data.get('params')

        if not method:
            return Response({
                "Error": "method kiritilmagan"
            })

        if params is None:
            return Response({
                "Error": "params kiritilmagan"
            })

        if method == "regis":

            mobile = params.get("mobile")
            user = User.objects.filter(mobile=mobile).first()

            if user:
                return Response({
                    "Error": "Bu tel nomer allaqachon bor"
                })

            serializer = self.get_serializer(data=params)
            serializer.is_valid(raise_exception=True)
            user = serializer.create(serializer.data)
            user.set_password(params["password"])
            user.save()

            token = Token()
            token.user = user
            token.save()

        elif method == "login":
            nott = 'mobile' if "mobile" not in params else "password" if "password" not in params else None
            if nott:
                return Response({
                    "Error": f"{nott} polyasi to'ldirilmagan"

                })

            mobile = params.get("mobile")
            user = User.objects.filter(mobile=mobile).first()

            if not user:
                return Response({
                    "Error": "Bunday User topilmadi"
                })
            if not user.check_password(params['password']):
                return Response({
                    "Error": "parol  xato"
                })
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token()
                token.user = user
                token.save()

        elif method == "step.one":
            nott = 'mobile' if "mobile" not in params else "lang" if "lang" not in params else None
            if nott:
                return Response({
                    "Error": f"params.{nott} polyasi to'ldirilmagan"

                })

            code = random.randint(10000, 99999)
            otp = code_decoder(code)
            sms = sms_sender(params['mobile'], code, params['lang'])
            if sms.get('status') != "waiting":
                return Response({
                    "error": "sms xizmatida qandaydir muommo",
                    "data": sms
                })

            root = OTP()
            root.mobile = params['mobile']
            root.key = "pbkdf2_sha256$" + otp + "$" + uuid.uuid1().__str__()
            root.save()

            return Response({
                "otp": code,
                "token": root.key
            }
            )


        else:
            return Response({
                "Error": "Bunday method yoq"
            })

        return Response({
            "result": {
                "token": token.key,
                "mobile": user.mobile,
                "name": user.ism,
            }
        })
