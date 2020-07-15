from django.urls    import path

from .views         import (
   CartAddView,
   CartListView
)

urlpatterns = [
    path('/cart', CartAddView.as_view()),
    path('/cartlist', CartListView.as_view()),
]