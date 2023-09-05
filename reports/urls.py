from django.urls import path
from .views import SummaryView,CategoryView,SentimentView


urlpatterns = [
    path('',  SummaryView.as_view()),
    path('filter', CategoryView.as_view()),
    # path('Sub-Category',SubCategoryView.as_view()),
    path('sentiment',SentimentView.as_view())
]
