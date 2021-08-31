from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from applications.users import urls as user_urls
from applications.accounts import urls as accounts_urls

# swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

description = """This is just a simple financial account API for hiring test
in a python senior job.

Some of this endpoints should have to pass a DRF Token
(basic token authentication) in header. The format is:

Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXX

Where XXXX is the passed user token created to the model"""
openapi_info = openapi.Info(
        title="Simple Financial Account API",
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
    path('authenticate', obtain_auth_token),
    # apps router control
    path('api/users/', include(user_urls)),
    path('api/accounts/', include(accounts_urls)),
    # swagger documentation
    path('swagger', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'),
]
