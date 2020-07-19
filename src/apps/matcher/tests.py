from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model as user_model
User = user_model()
from rest_framework.test import force_authenticate
import io
from rest_framework.parsers import JSONParser
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
import os
class MatcherBasicTest(APITestCase):

    def setUp(self):
        # create user
        self.user = User(username='a')
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        pass

    def testDetailViewBasicFunctionality(self):
        # os.path.join
        base_path = os.path.dirname(os.path.realpath(__file__))
        print(base_path)
        pat = base_path + "/medicalRecords.csv"
        print(pat)
        # base = os.path.join(base, '/matcher')
        # print(base)
        data = open(pat, 'rb')
        file = SimpleUploadedFile("medicalRecords.csv", data.read(), content_type="text/csv")
        response = self.client.post('/matcher/', {'file': file})
        print(response.data)
