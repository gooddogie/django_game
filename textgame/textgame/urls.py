from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),  # URL для административной панели Django
    path('', include('game.urls')), 
]
