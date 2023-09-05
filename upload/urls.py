from django.urls import path
from . views import FileUploadView


urlpatterns = [
    path('',  FileUploadView.as_view()),    
    path('<pk>',  FileUploadView.as_view())    
]
