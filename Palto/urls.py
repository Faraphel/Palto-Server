"""
URL configuration for Palto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve

from Palto import settings
from Palto.Palto import urls as palto_views_urls
from Palto.Palto.api import urls as palto_api_urls


urlpatterns = [
    # Application
    path('', include(palto_views_urls)),

    # API
    path('api/', include(palto_api_urls)),  # Api REST

    # Debug
    path('admin/', admin.site.urls),  # Admin page
    path("__debug__/", include('debug_toolbar.urls')),  # Debug toolbar
]


if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]
