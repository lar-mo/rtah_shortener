from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('url_shortener.urls')),
    path(r'captcha/', include('captcha.urls'))
]
