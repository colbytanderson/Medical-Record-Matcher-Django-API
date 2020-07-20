from rest_framework import serializers

from .models import Record, Column

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['title', 'confidenceScore']
    def create(self, validated_data):
        """
        
        """
        user = self.context['request'].user
        record = Record.objects.create(**validated_data,
            owner=user)
        return record

class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['title', 'confidenceScore', 'dataType', 'skip']