from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from rest_framework.schemas import get_schema_view

api_urls = [
    path("users/", include("users.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urls)),
    path("openapi", get_schema_view(
        title="Zeton project",
        description="API for Zeton React client",
        version="0.0.1",
    ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
]
