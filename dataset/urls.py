from django.urls import path
from .views import DefaultDatasetView


urlpatterns = [
    path('default',  DefaultDatasetView.as_view())    
]
