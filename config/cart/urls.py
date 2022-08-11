from django.urls import path

from .views import cart_detail, cart_add, cart_remove
app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<uuid:product_id>/', cart_add, name='cart_add'),
    path('remove/<uuid:product_id>/', cart_remove, name='cart_remove'),
]
