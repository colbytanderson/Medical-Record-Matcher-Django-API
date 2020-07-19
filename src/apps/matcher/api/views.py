from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class MatchMedicalRecordsView(APIView):
    """
    A view for authenticated users. It allows users to upload
    a CSV file and get back the matches as an array.
    """
    def get(self, request, format=None):
        """
        Handles get requests. Request is a CSV file. Returns an
        error if CSV is improperly formatted or if the file is not
        a CSV file. Otherwise, it will attempt to find likely matches
        based off of many algorithms.
        """
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            # error