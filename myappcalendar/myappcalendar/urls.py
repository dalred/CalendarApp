from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


from users.views import root

urlpatterns = [
    path('', root),
    path('admin/', admin.site.urls),
    path("core/", include("users.urls")),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('core/', include('login.urls')),
    path("oauth/", include("social_django.urls", namespace="social"))
]
