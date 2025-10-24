from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clubs/', include('ibeth_clubs.urls', namespace='clubs')),
    path('auth/', include('authentication.urls', namespace='authentication')),  
]
