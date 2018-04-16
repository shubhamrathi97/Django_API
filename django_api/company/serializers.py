from rest_framework import serializers

from . import models


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        fields = ('id', 'company_name', 'addresses')
        model = models.Company


class PostalCodeSerializer(serializers.Serializer):
    postal_code = serializers.IntegerField()
    count = serializers.IntegerField()
