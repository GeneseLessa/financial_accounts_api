from django.urls import path
from applications.senders.views import SendView

# swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

description = """This is just a simple message API for suport hiring test
in a python senior job.
"""
openapi_info = openapi.Info(
        title="Message API for Account Support",
        default_version='v1',
        description=description,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="genese.lessa@xyz.local"),
        license=openapi.License(name="BSD License"),
    )

schema_view = get_schema_view(
    openapi_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('sender', SendView.as_view()),
    # swagger documentation
    path('swagger', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'),
]
