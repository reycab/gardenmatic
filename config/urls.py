"""Base URLs."""
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from app.common import errors as middleware
from app.gardenmatic import views

handler500 = middleware.error_500
handler404 = middleware.error_404

router = routers.DefaultRouter()
router.register(
    r'sensores-disponibles', views.SensoresDisponiblesApiViewSet,
    'sensores-disponibles')


urlpatterns = [
    path(r'accounts/', include('allauth.urls')),
    path(r'accounts/', include('app.accounts.urls', namespace='accounts')),
    path(r'api/', include(router.urls)),
    path(r'api/reading-sensor/', views.reading_sensor),
    # path(r'', include('app.site.urls', namespace='site')),
    path(r'', include('app.gardenmatic.urls', namespace='gardenmatic')),
    path(r'api-auth/', include('rest_framework.urls')),
    # path(r'i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += i18n_patterns(
    # ...
    # ...
    # If no prefix is given, use the default language
    prefix_default_language=True
)
