from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from social_network_api.models import Post
from social_network_api.serializers import AccountRegistrationSerializer, PostDetailSerializer, PostLikeSerializer


class RegistrationView(APIView):
    def post(self, request):
        serializer = AccountRegistrationSerializer(data=request.data)
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


class PostLikesView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        post = Post.objects.filter(pk=pk).first()
        data = {}
        if request.user.is_authenticated:
            data['user_id'] = request.user.id
            serializer = PostLikeSerializer(instance=post, data=data, partial=True)
            if serializer.is_valid():
                liked_post = serializer.save()
            else:
                return Response(serializer.errors)
            if request.user in liked_post.users_likes.all():
                like_str = 'like'
            else:
                like_str = 'unlike'
            return Response({"success": "Post {} {} by {}".format(liked_post.title, like_str, request.user)})
        else:
            return Response("User auth error")
