from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'account'
urlpatterns = [
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/signup/', views.SignupApi.as_view(), name='signup'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('update', views.UpdateAccountView.as_view(), name='update_account'),

    path('auth/change-password', views.ChangePasswordView.as_view(), name='change-password'),

]