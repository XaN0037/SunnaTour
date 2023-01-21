from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.v1.auth.serializer import Userserializer
from api.models import User


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
            root = serializer.create(serializer.data)
            root.set_password(params["password"])
            root.save()

            token = Token()
            token.user = root
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
        else:
            return Response({
                "Error": "Bunday method yoq"
            })

        return Response({
            "result": {
                "toker": token.key,
                "mobile": user.mobile,
                "name": user.ism,
            }
        })
