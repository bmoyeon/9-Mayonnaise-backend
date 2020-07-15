
from django.urls import path, include


urlpatterns = [
   
   path('product', include('product.urls')),
   path('account', include('account.urls')),
   path('order'  , include('order.urls'))
  

]
