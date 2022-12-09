import django
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from corn.factories import CornFactory


class YieldViewTests(APITestCase):
    def test_corn_list(self):
        batch_size = 10
        CornFactory.create_batch(batch_size)
        url = reverse("corn_list")
        response = self.client.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == batch_size
