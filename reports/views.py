from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from upload.models import DataSet
from upload.serializers import DataSetSerializer
from .serializers import ResultSerializer
from .models import Result
from rest_framework import status
from . import reportBl
import json
import pandas as pd
import numpy as np

class SummaryView(APIView):
    def get(self, request):
        # get default dataset id.
        try:
            default_dataset = DataSet.objects.get(isDefault = True)
        except:
            return Response(status=status.HTTP_200_OK, data={"status": "success", "data": []})       
            
        serializedData = DataSetSerializer(default_dataset)                
        default_dataset_id = serializedData.data['id']                
        # get summary from reports_result table with dataset id.        
        try:
            summary_data = Result.objects.get(datasetId= default_dataset_id)
        except:
            return Response({"status": "success", "data": []})    

        result_serializer = ResultSerializer(summary_data)        
        return Response({"status": "success", "data": result_serializer.data})

class CategoryView(APIView):
    def get(self, request):
        filter = request.query_params.get('filter')
        result = reportBl.getCategoryReport("media/testData.xlsx", filter)
        return Response({"status": "success", "data": result})

class SentimentView(APIView):
    def get(self,request):        
        filter = request.query_params.get('filter')
        result=reportBl.getSentiment("media/testData.xlsx", filter)        
        return Response({"status":"success","data":result})
