from django.urls import path
from .views import portada, procesar_carrito, checkout, procesar_pedido

urlpatterns = [
    path('', portada, name='portada'),
    path('checkout/', checkout, name='checkout'),
    path('procesar-carrito/', procesar_carrito, name='procesar_carrito'),
    path('procesar-pedido/', procesar_pedido, name='procesar_pedido')
]