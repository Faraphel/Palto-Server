"""
Urls for the Palto project's API.

This file list all the urls for the Palto API.
"""

from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

import Palto.Palto.api.v1.urls as v1_urls

app_name = "PaltoAPI"

urlpatterns = [
    # Authentification (JWT)
    path('auth/jwt/token/', TokenObtainPairView.as_view(), name='token'),
    path('auth/jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/jwt/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # API
    path('v1/', include(v1_urls)),
]
