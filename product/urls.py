from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('products', views.ProductsView.as_view(), name='product_list'),
    path('product/<int:id>', views.ProductView.as_view(), name='product_detail'),
    path('product/<int:id>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('<int:id>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('create/', views.CreateProductView.as_view(), name='product_create'),
    path('categories', views.CategoriesView.as_view(), name='category_list'),
    path('subcategories', views.SubCategoriesView.as_view(), name='subcategory_list'),
    path('sub-subcategories', views.Sub_SubCategoriesView.as_view(), name='sub_subcategory_list'),
    path('category/<str:slug>', views.CategoryView.as_view(), name='category'),
    path('subcategory/<str:slug>/<str:category>', views.SubCategoryView.as_view(), name='subcategory'),
    path('sub-subcategory/<str:slug>/<str:subcategory>', views.Sub_SubCategoryView.as_view(), name='sub_subcategory'),
]   