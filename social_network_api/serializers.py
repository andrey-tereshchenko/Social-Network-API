from rest_framework import serializers
from social_network_api.models import Account
from django.contrib.auth.models import User


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
            email=self.validated_data['email'],
        )
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
