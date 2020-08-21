from django.urls import path

from .views import (
    ReservationView,
    ReservationCheckView,
    ReservationUpdateView
)

urlpatterns = [
    path('', ReservationView.as_view()),
    path('/check', ReservationCheckView.as_view()),
    path('/update', ReservationUpdateView.as_view())
]
