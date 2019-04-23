# from django.conf.urls import url

from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [

     path('search/', views.SearchView.as_view(), name='search'),
     path('<int:product_id>/result/', views.ResultView.as_view(), name='result'),
     path('save/', views.SaveView, name='save'),
     path('delete/<int:pk>', views.DeleteSubstituteView.as_view(), name='delete'),
     path('<int:pk>/detail/', views.DetailProductView.as_view(), name='detail'),
     path('myproducts/', views.MyProductsView.as_view(), name='myproducts'),
]
