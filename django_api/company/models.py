from django.db import models


class Company(models.Model):
    company_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.company_name


class Address(models.Model):
    company = models.ForeignKey(Company, related_name='addresses', on_delete=models.CASCADE)
    building = models.TextField()
    postal_code = models.IntegerField()
    locality = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
