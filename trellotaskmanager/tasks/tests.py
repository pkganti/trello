# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

import pdb
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from .models import Team
from profiles.models import Profile
from .serializers import TeamSerializer

# Create your tests here.

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_team(name=""):
        if name != "":
            # First Create a Test User with Profile
            user = User.objects.create_user('test_user', 'testing@test.com', 'testpassword')
            profile = Profile.objects.get(user=user)
            profile.first_name = "TestFirstName"
            profile.last_name = "TestLastName"
            profile.save()
            # Here since team should be having an ID before we assign profiles to it and hence we create the team first and assign the profile id to it
            team = Team.objects.create(name=name)
            team.members.add(profile.id)
            team.save()

    def setUp(self):
        self.create_team("Team1")


class GetAllTeamsTest(BaseViewTest):

    def test_get_all_teams(self):
        """
        This test ensures all the teams are added in the setUp
        method exists when we make a GET requests to teams/ endpoint
        """

        response = self.client.get(
            reverse("teams-all")
        )

        expected = Team.objects.all()
        serialized = TeamSerializer(expected, many=True)

        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
