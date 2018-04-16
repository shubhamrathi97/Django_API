from django.urls import re_path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from . import views

router = routers.DefaultRouter(trailing_slash=True)
router.register(r'company', views.CompanyList, base_name="company")
router.register(r'address', views.AddressList, base_name="address")
router.register(r'postalcode/(?P<count>[0-9]+)', views.PostalCodeList, base_name="postalcode")


urlpatterns = [
    re_path(r'', include(router.urls)),
    re_path(r'^docs/', include_docs_urls(title='Django API Doc'))
]
