from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    # path('row_transposition_cipher', views.row_transposition_cipher),
]