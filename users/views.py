from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from users.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from oauth2_provider.settings import oauth2_settings
from braces.views import CsrfExemptMixin
from oauth2_provider.views.mixins import OAuthLibMixin
from django.core import serializers

import json
# import models
from users.serializers import RegisterSerializer

from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.translation import gettext_lazy as _
from django.db import transaction
import users.usersBl as usersBl

class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    def get(self, request, format=None):
        """
            Return a list of all users
        """
        queryset = User.objects.all().order_by('-date_joined')                
        serializer = UserSerializer(queryset, many=True)        
        usersBl.my_func(10)
        return Response(serializer.data)

class UserViewSet(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    def get(self, request):
        # current_user = request.user
        # print("working..")
        username = request.GET.get('username')
        queryset = User.objects.get(username=username)
        serializer_class = UserSerializer(queryset) 
        return Response(serializer_class.data)
        # return Response("hello")

class UserRegister(CsrfExemptMixin, OAuthLibMixin, APIView):
    permission_classes = (permissions.AllowAny,)

    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def post(self, request):
        if request.auth is None:
            data = request.data
            serializer = RegisterSerializer(data=data)
            if serializer.is_valid():
                try:
                    user = User.objects.create_user(
                        username=data.get('username'),
                        email=data.get('email'),
                        first_name=data.get('firstName'),
                        last_name=data.get('lastName'),
                        password=data.get('password'))
                    return Response(data={"status": "success"})
                except Exception as e:
                    return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)
