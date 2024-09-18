from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.project.settings import ADMIN_PATH, DEBUG  # noqa: I101
from core.project.settings.utils_config import MEDIA_ROOT, MEDIA_URL  # type: ignore

from .utils.api_setup import schema_view

urlpatterns = [
    path(f'{ADMIN_PATH}/', admin.site.urls),
    path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/', include('core.api.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Add paths in debug mode
if DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + static(MEDIA_URL, document_root=MEDIA_ROOT)
