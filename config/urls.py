"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
#from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reservations.urls')),  # URLs principales
    path('api/', include([
        path('', include('reservations.api_urls')),  # URLs API
        #path('docs/', include_docs_urls(title='API de Réservation', public=False)),
    ])),
]
