from django.urls import path

from . import views

app_name = 'url_shortener'
urlpatterns = [
    # rtah.xyz/
    path('', views.index, name='index'),
    # rtah.xyz/saveurl
    path('saveurl/', views.saveurl, name='saveurl'),
    # rtah.xyz/abc123/
    path('<str:code>/', views.redir_to_long_url, name='redir_to_long_url'),
]
