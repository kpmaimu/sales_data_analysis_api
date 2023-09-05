from rest_framework import serializers
from .models import File, DataSet


class FileSerializer(serializers.ModelSerializer):
    class Meta():
        model = File
        fields = ('file', 'remark', 'timestamp')

class DataSetSerializer(serializers.ModelSerializer):
    class Meta():
        model = DataSet
        fields = ('id','name', 'url', 'columns', 'isProcessed', 'fileSize', 'createdBy', 'createdOn', 'isActive','isDefault')