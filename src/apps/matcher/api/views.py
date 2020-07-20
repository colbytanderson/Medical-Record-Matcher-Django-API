from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.matcher.start import main
from io import BytesIO
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.matcher.main.models import Record, Column
from apps.matcher.main.serializers import RecordSerializer, ColumnSerializer
from rest_framework.decorators import action

class RecordModelViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def addColumn(self, request, pk):
        """
        
        """
        record = self.get_object()
        if not record.editors.contains(request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = ColumnSerializer(request.data)
        if serializer.is_valid():
            title = serializer.validated_data['title']
            confidenceScore = serializer.validated_data['confidenceScore']
            dataType = serializer.validated_data['dataType']
            new_column = Column(title=title, confidenceScore=confidenceScore,
                                dataType=dataType, record=record)
            new_column.save()

    @action(detail=True, methods=['post'])
    def matchRows(self, request, pk):
        """
        Handles get requests. Request is a CSV file. Returns an
        error if CSV is improperly formatted or if the file is not
        a CSV file. Otherwise, it will attempt to find likely matches
        based off of many algorithms.
        """
        csv_file = request.FILES['file']
        record = self.get_object()
        if not csv_file.name.endswith('.csv'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            columns = record.column_set.order_by('index')
            print(columns)
            formattedCSV = csv_file.read().decode('utf-8').splitlines()
            ret = main(formattedCSV, columns, record.confidenceScore, record.fullNameConfidenceScore)
            return Response(data=ret, status=status.HTTP_200_OK)