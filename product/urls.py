from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('products/', views.ProductsView.as_view(), name='product_list'),
    path('products/create/', views.CreateProductView.as_view(), name='product_create'),
]