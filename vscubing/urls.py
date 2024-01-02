from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/swagger/', include('apps.swagger.urls')),
    path('api/accounts_app/', include('apps.accounts.urls')),
    path('api/contests_app/', include('apps.contests.urls')),
]
