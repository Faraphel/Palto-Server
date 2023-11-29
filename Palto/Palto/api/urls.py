from django.urls import path, include
import Palto.Palto.api.v1.urls as v1_urls

urlpatterns = [
    # API
    path('v1/', include(v1_urls)),
]
