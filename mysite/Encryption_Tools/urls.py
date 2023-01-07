from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('/text_hex', views.text_hex),
    path('/mod_inv', views.mod_inv),
    path('/exponentiation', views.exponentiation_func),
    path('/gfo', views.gfo),
    # path('row_transposition_cipher', views.row_transposition_cipher),
]