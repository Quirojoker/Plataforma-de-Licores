from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('categoria/<int:categoria_id>/', views.categoria_productos, name='categoria_productos'),
    path('categoria/<int:categoria_id>/orden/<str:orden>/', views.categoria_productos, name='categoria_productos_orden'),
]

