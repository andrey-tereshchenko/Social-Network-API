from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from social_network_api.serializers import UserRegistrationSerializer, AccountRegistrationSerializer


# @api_view(['POST', ])
# def registration_view(request):
#     if request.method == 'POST':
#         serializer = AccountRegistrationSerializer(data=request.data)
#         data = {}
#         if serializer.is_valid():
#             account = serializer.save()
#             data['response'] = 'Successfully registered new user'
#             data['username'] = account.user.username
#             data['email'] = account.user.email
#         else:
#             data = serializer.errors
#         return Response(data)


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
