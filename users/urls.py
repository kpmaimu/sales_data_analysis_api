from django.urls import path
from . views import UserRegister, UserViewSet, ListUsers


urlpatterns = [
    path('', ListUsers.as_view()),
    path('register/', UserRegister.as_view()),
    path('loggedin/', UserViewSet.as_view())
]
