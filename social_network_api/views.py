from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from social_network_api.serializers import AccountRegistrationSerializer, PostDetailSerializer


class RegistrationView(APIView):
    def post(self, request):
        serializer = AccountRegistrationSerializer(data=request.data)
        print(serializer)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'Successfully registered new user'
            data['username'] = account.user.username
            data['email'] = account.user.email
        else:
            data = serializer.errors
        return Response(data)


class PostCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostDetailSerializer
