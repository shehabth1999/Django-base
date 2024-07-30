from django.urls import path, include
from django.conf import settings

VERSION = settings.API_VERSION

urlpatterns = [
    path(f'api-{VERSION}/', include('accounts.api.urls')),
]