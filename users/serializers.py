from django.contrib.auth.models import User, Group
from rest_framework import serializers
# import models
# from users.models import u
from django.utils.translation import gettext_lazy as _

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        # fields = ('url', 'username', 'email', 'groups')
        fields = ('username', 'email', 'first_name', 'last_name')

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.filter(username=data.get('username'))
            if len(user) > 0:
                raise serializers.ValidationError(_("Username already exists"))
        except User.DoesNotExist:
            pass

        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError(_("Empty Password"))

        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError(_("Mismatch"))

        return data

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'confirm_password', 'is_active')
        # fields = ('username', 'first_name', 'last_name', 'password', 'is_active')
        extra_kwargs = {'confirm_password': {'read_only': True}}