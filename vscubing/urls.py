from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', include('apps.swagger.urls')),
    path('accounts/', include('apps.accounts.urls')),
    # path('contests/', include('apps.contests.urls')),
]
