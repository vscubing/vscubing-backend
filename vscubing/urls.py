from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/swagger/', include('apps.swagger.urls')),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/contests/', include('apps.contests.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
