from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('products', views.ProductsView.as_view(), name='product_list'),
    path('create/', views.CreateProductView.as_view(), name='product_create'),
    path('categories', views.CategoriesView.as_view(), name='category_list'),
    path('subcategories', views.SubCategoriesView.as_view(), name='subcategory_list'),
    path('sub-subcategories', views.Sub_SubCategoriesView.as_view(), name='sub_subcategory_list'),
]