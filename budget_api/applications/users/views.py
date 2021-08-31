from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User


class CreateUser(APIView):
    """This view can create user by the POST HTTP"""

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User(**serializer.data)
            user.set_password(user.password)
            user.is_active = True
            user.save()

            return Response(UserSerializer(user).data)
        else:
            return Response(data=serializer.errors)


class ReadUser(APIView):
    """This view update and read one or more users"""

    def get(self, request, id=None):
        user = User.objects.get(pk=id) if id else User.objects.all()
        return Response(UserSerializer(user, many=(id is None)).data)
