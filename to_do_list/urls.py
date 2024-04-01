from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('www.urls')),
    path('api/auth/', include('users.urls'))
]
