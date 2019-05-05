# from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
# from .forms import AuthenticationFormEmail


app_name = 'authentication'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('modify/', views.ModifyView.as_view(), name='modify'),
]
