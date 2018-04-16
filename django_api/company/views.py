from django.db.models import Count
from rest_framework import generics, viewsets
from rest_framework.response import Response

from . import models
from . import serializers


class CompanyList(viewsets.ModelViewSet):
    """
      retrieve:
      Return the company profile.

      list:
      Return a list of all the existing company.
      Company_name and City params can be passed with URL.
        "company_name Filter" : -
            Return the company profile with Address on providing company name as param
            Example:-  /company?company_name=Hello
        "city Filter": -
            Return the company profile in a particular city
            Example:-  /company?city=Bhopal

      create:
      Create a new company.
    """
    serializer_class = serializers.CompanySerializer

    def get_queryset(self):
        queryset = models.Company.objects.all()
        if self.request.query_params.get('city', None):
            Addresses = models.Address.objects.filter(city__icontains=self.request.query_params.get('city'))
            company_ids = set([Address.company.id for Address in Addresses])
            queryset = models.Company.objects.filter(id__in=company_ids)
        if self.request.query_params.get('company_name', None):
            queryset = models.Company.objects.filter(company_name__icontains=self.request.query_params.get('company_name'))
        return queryset


class AddressList(viewsets.ModelViewSet):
    queryset = models.Address.objects.all()
    serializer_class = serializers.AddressSerializer


class PostalCodeList(viewsets.ViewSet):
    """
    list:
        Return a list of postalcode have companies greater than count.
        Count is provided in URL Params
        Example :- /postalcode/{count}/
    """
    def list(self, request, count):
        queryset = models.Address.objects.values('postal_code').annotate(count=Count('company', distinct=True))\
            .filter(count__gte=count)
        serializer = serializers.PostalCodeSerializer(queryset, many=True)
        return Response(serializer.data)