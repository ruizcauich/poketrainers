from http import client
import json
import logging
from faker import Faker

from django.test import TestCase
from django.urls import reverse
from rest_framework import status, test

import core.models


logger = logging.getLogger(__name__)

class ApiRootTest(TestCase):
    """Tests api root endpoint.
    """

    def setUp(self) -> None:
        logger.debug("Seting up APIRootTest")
        self.client = test.APIClient()
        return super().setUp()

    def test_succes_get_api_root(self):
        """Test that requesting the api root returns ok.
        """
        logger.debug("Executing test_succes_get_api_root")
        response = self.client.get('/api/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_get_all_api_routes(self):
        """Test that the api root returns three endpoints.
        """
        logger.debug("Executing test_get_all_api_routes")

        response = self.client.get('/api/')

        self.assertContains(response, b'/api/teams/')
        self.assertContains(response, b'/api/pokemon/')
        self.assertContains(response, b'/api/trainers/')
        
        
class TestTrainersEndpoint(TestCase):
    """Test the trainers endpoint"""

    def setUp(self):
        logger.debug("Setting up TestTrainerEndpoint")
        self.cliet = test.APIClient()

        # Use faker to randomly get fake info
        self.faker = Faker()

        for _ in range(10):
            core.models.PokemonTrainer.objects.create(
                name=self.faker.name, hometown=self.faker.city)
        
    def test_get_ten_trainers(self):
        """Tests that trainers endpoint returns 10 objects.
        """
        logger.debug("Executing test_get_ten_trainers")

        response = self.client.get('/api/trainers/')

        trainers_list_length = len(response.data['results']) 
        self.assertEqual(10, trainers_list_length)

    def test_next_url_is_none(self):
        """Test that the 'next' url is None
        
        The API is paginated, but will return next url if
        the results are more than 100
        """
        logger.debug("Executing test_next_url_is_none")

        response = self.client.get('/api/trainers/')
        self.assertEqual(response.data['next'], None)

    def test_next_url_is_not_none(self):
        """Test that response has a 'next' url
        
        The API is paginated, but will return next url if
        the
        """
        logger.debug("Executing test_next_url_is_not_none")
        for _ in range(100):
            core.models.PokemonTrainer.objects.create(
                name=self.faker.name,
                hometown=self.faker.city
            )
        
        response = self.client.get('/api/trainers/')
        # logger.info(response.data)
        self.assertContains(response, b'/api/trainers/?limit=100&offset=100')