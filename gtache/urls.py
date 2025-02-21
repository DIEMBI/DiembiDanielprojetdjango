from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
urlpatterns = [
    path('admin/', admin.site.urls),
    path('tache/', include('tache.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('tache.urls')),  
    path('', lambda request: redirect('projects/', permanent=True)),

]
