from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('/', views.index),
    path('/text_hex', views.text_hex),
    path('/mod_inv', views.mod_inv),
    path('/exponentiation', views.exponentiation_func),
    path('/gfo', views.gfo),
    path('/caesar', views.cipher_caesar),
    path('/affine', views.cipher_affine),
    path('/hill', views.cipher_hill),
    path('/playfair', views.cipher_playfair),
    path('/viginere', views.cipher_viginere),
    path('/monoalphabetic', views.cipher_monoalphabetic),
    path('/railfence', views.cipher_railfence),
    path('/rowtrans', views.cipher_rowtrans),
    path('/aes', views.aes_func),
    path('/des', views.des_func),
    path('/ecb', views.ecb_func),
    path('/cbc', views.cbc_func),
    path('/ofb', views.ofb_func),
    path('/dselgamal', views.ds_eg),
    path('/ecdsa', views.ecdsa),
    # path('row_transposition_cipher', views.row_transposition_cipher),
]