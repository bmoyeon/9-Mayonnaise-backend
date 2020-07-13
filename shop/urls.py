from .views import shopListView
from django.urls import path

urlpatterns = [
    path('/', shopListView.as_view()),
]
