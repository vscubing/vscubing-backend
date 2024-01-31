from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/legacy-contests/', include('apps.legacy_contests.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name='schema'))
]
