from django.urls import path

from .views import (
    MenuView,
    CategoryView,
    ProductListView,
    ProductDetailView
)

urlpatterns = [
    path('/menu', MenuView.as_view()),
    path('/category', CategoryView.as_view()),
    path('/list', ProductListView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
]
