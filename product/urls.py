from django.urls import path
from .views import *


urlpatterns = [
    path('all', ProductListView.as_view()),
    path('s/<str:query>', SearchProduct.as_view()),
    path('<str:productId>', GetProduct.as_view()),
    path('filter/<str:filterQuery>', FilterProduct.as_view())
]