from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.reverse import reverse
from . import models
import urllib

def build_url(*args, **kwargs):
    get = kwargs.pop('get', {})
    url = reverse(*args)
    if get:
        url += '?' + urllib.parse.urlencode(get)
    return url

class ModelTestCase(TestCase):
    """This class defines the test suite for the company and address model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.company_name = "Hello Company"
        self.company = models.Company(company_name=self.company_name)

    def test_model_can_create_a_company(self):
        """Test the company model can create a company."""
        old_count = models.Company.objects.count()
        self.company.save()
        new_count = models.Company.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_create_a_address_for_company(self):
        """Test the address model can create a address."""
        self.company = models.Company.objects.first()
        if not self.company:
            self.company_name = "Hello Company"
            self.company = models.Company(company_name=self.company_name)
            self.company.save()
        self.company_address = {
            "building": "abc",
            "postal_code": 123456,
            "locality": "Hello",
            "city": "Hello",
            "state": "World",
            "company": self.company
        }
        self.address = models.Address(**self.company_address)
        old_count = models.Address.objects.count()
        self.address.save()
        new_count = models.Address.objects.count()
        self.assertNotEqual(old_count, new_count)


# Create your tests here.
class CompanyViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.company_data = {'company_name': 'Hello World'}
        self.response = self.client.post(
            reverse('company-list'),
            self.company_data,
            format="json")

    def test_api_can_create_a_company(self):
        """Test the api has company registration capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_company(self):
        """Test the api can return company list."""
        companylist = models.Company.objects.get()
        response = self.client.get(
            reverse('company-detail',
                    kwargs={'pk': companylist.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_filter_by_company_name(self):
        """"""
        company_data = {'company_name': 'Second Company'}
        company_second = models.Company(**company_data)
        company_second.save()
        self.response = self.client.get(
            build_url('company-list',
                    get={'company_name': "second"}),
            format="json")
        self.assertEqual(self.response.data[0]["company_name"], company_data["company_name"])


    def test_api_can_update_company(self):
        """Test the api can update a given company"""
        company = models.Company.objects.get()
        change_company_name = {'company_name': 'Something new'}
        res = self.client.put(
            reverse('company-detail', kwargs={'pk': company.id}),
            change_company_name, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_company = models.Company.objects.get()
        self.assertEqual(new_company.company_name, change_company_name['company_name'])

    def test_api_can_delete_company(self):
        """Test the api can delete a company"""
        company = models.Company.objects.get()
        response = self.client.delete(
            reverse('company-detail', kwargs={'pk': company.id}),
            format='json',
            follow=True)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

class AddressViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.company = models.Company.objects.first()
        if not self.company:
            self.company = models.Company(company_name="Testing Company")
            self.company.save()
        self.client = APIClient()
        self.company_address = {
            "building": "abc",
            "postal_code": 123456,
            "locality": "Hello",
            "city": "Hello",
            "state": "World",
            "company": self.company.id
        }
        self.response = self.client.post(
            reverse('address-list'),
            self.company_address,
            format="json")
        self.address = models.Address.objects.get()

    def test_api_can_add_address_of_company(self):
        """Test the api can add address of company"""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_address(self):
        """Test the api can return address."""
        response = self.client.get(
            reverse('address-detail',
                    kwargs={'pk': self.address.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertContains(response, address)

    def test_api_can_update_address(self):
        """Test the api can update a given address"""
        self.company_address["city"] = "Bhopal"
        res = self.client.put(
            reverse('address-detail', kwargs={'pk': self.address.id}),
            self.company_address, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_address = models.Address.objects.get()
        self.assertEqual(new_address.city, self.company_address.get('city'))

    def test_api_can_delete_address(self):
        """Test the api can delete a address"""
        response = self.client.delete(
            reverse('address-detail', kwargs={'pk': self.address.id}),
            format='json',
            follow=True)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)


class PostalCodeTestCase(TestCase):
    """Test suite for the api views."""
    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.company = models.Company(company_name="Testing Company")
        self.company.save()
        self.company_address = {
            "building": "abc",
            "postal_code": 123456,
            "locality": "Hello",
            "city": "Hello",
            "state": "World",
            "company": self.company
        }
        self.company_address = models.Address(**self.company_address)
        self.company_address.save()

    def test_api_can_get_postalcode(self):
        """Test the api can return list of pincode"""
        response = self.client.get(
            reverse('postalcode-list',
                    kwargs={'count': 1}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    def test_api_can_get_postalcode(self):
        """Test the api can return list of pincode"""
        response = self.client.get(
            reverse('postalcode-list',
                    kwargs={'count': 2}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
