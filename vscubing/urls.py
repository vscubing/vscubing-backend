from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/swagger/', include('apps.swagger.urls')),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/contests/', include('apps.contests.urls')),
]
