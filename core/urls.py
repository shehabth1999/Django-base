"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

VERSION = settings.API_VERSION

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG: 
    schema_view = get_schema_view(
   openapi.Info(
      title=admin.site.site_title,
      default_version=VERSION,
    #   description="Test description",
    #   terms_of_service=settings.ALLOWED_HOSTS[0],
    #   contact=openapi.Contact(email="mohamed.arafa176@snippets.local"),
    #   license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
    )

    urlpatterns +=[
        # Toolbar
        path('__debug__/', include(debug_toolbar.urls)),
        # Swagger
        path('swagger/', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
        # path('api/api.json/', schema_view.without_ui(cache_timeout=0),name='schema-swagger-ui'),
        #url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),

        path(
        'swagger.json',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
        ),
            path('redoc/', schema_view.with_ui('redoc',cache_timeout=0), name='schema-redoc'),
    ]