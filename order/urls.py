from django.urls import path
from . import views

app_name='order'
urlpatterns = [
    path('add-to-order/', views.AddToOrderItem.as_view(), name='add_to_order'),
    path('order', views.OrdersView.as_view(), name='order_list'),
    path('<int:orderitem_id>/delete/', views.DeleteOrderItem.as_view(), name='delete_cartitem'),
]