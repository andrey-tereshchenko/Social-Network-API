from rest_framework import serializers
from social_network_api.models import Account, Post
from django.contrib.auth.models import User
import requests


def is_exist_email(email):
    key = 'YOUR_API_KEY'
    response = requests.get('https://api.hunter.io/v2/email-verifier',
                            params={'email': str(email), 'api_key': key})
    json_response = response.json()
    if json_response['data']['result'] in ("deliverable", "risky"):
        return True
    else:
        return False


class UserRegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_confirm')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
        )
        email = self.validated_data['email']
        if is_exist_email(email):
            user.email = email
        else:
            raise serializers.ValidationError({'email': 'Email does not exist.'})
        password = self.validated_data['password']
        password_confirm = self.validated_data['password_confirm']
        if password != password_confirm:
            raise serializers.ValidationError({'password': 'Password must match.'})
        user.set_password(password)
        user.save()
        return user


class AccountRegistrationSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer(required=True)

    class Meta:
        model = Account
        fields = ('user', 'birthday',)

    def save(self):
        user_data = self.validated_data['user']
        user = UserRegistrationSerializer(data=user_data)
        if not user.is_valid():
            raise serializers.ValidationError({'user': 'User invalid.'})
        user = user.save()
        account = Account(
            user=user,
            birthday=self.validated_data['birthday'],
        )
        account.save()
        return account


class PostDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ('title', 'description', 'image', 'created_by')


class PostLikeSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ('user_id',)

    def update(self, instance, validated_data):
        user = User.objects.filter(id=validated_data['user_id']).first()
        if user in instance.users_likes.all():
            instance.users_likes.remove(user)
        else:
            instance.users_likes.add(user)
        instance.save()
        return instance
