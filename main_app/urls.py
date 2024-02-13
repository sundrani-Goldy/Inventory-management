import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions
from drf_yasg import openapi
from main_app.views.customer import CustomerView
from rest_auth.views import LogoutView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from main_app.views.customregister import CustomRegister

schema_view = get_schema_view(
    openapi.Info(
        title="Inventory API",
        default_version='v1',
        description="Multi Tenant APIs ",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    url=os.environ.get("SWAGGER_API_URL")
)
router = routers.DefaultRouter()
router.register(r'customer',CustomerView,basename='customer')


urlpatterns = [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    re_path(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    re_path(
        r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
    path("", schema_view.with_ui('swagger', cache_timeout=0)),
    path('api/', include(router.urls)),
    path("admin/", admin.site.urls),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', CustomRegister.as_view(), name='rest_register'),
    path('rest-auth/password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('rest-auth/password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('rest-auth/password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('rest-auth/logout/', LogoutView.as_view(), name='logout'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
