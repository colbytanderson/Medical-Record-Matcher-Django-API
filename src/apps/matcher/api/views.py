from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.matcher.main import main
from io import BytesIO

class MatchMedicalRecordsView(APIView):
    """
    A view for authenticated users. It allows users to upload
    a CSV file and get back the matches as an array.
    """
    def post(self, request, format=None):
        """
        Handles get requests. Request is a CSV file. Returns an
        error if CSV is improperly formatted or if the file is not
        a CSV file. Otherwise, it will attempt to find likely matches
        based off of many algorithms.
        """
        csv_file = request.FILES['file']
        # print(request.data['file'])
        print(request.FILES['file'])
        if not csv_file.name.endswith('.csv'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            # a = BytesIO(csv_file.read())
            # print(a)
            # b = str(csv_file.read())
            ret = main(csv_file.read().decode('utf-8').splitlines())
            print(ret)
            return Response(data=ret, status=status.HTTP_200_OK)