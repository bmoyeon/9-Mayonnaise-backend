from .views import ReivewView
from django.urls import path

urlpatterns = [
    path('', ReivewView.as_view()),
]
