from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser, FileUploadParser
from .serializers import FileSerializer, DataSetSerializer
from reports.serializers import ResultSerializer
from rest_framework import status
from rest_framework.views import APIView
import pandas as pd
import xlrd
import html5lib
import os
from reports import reportBl
from .models import DataSet
from reports.models import Result
import json

# Create your views here.


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        uploadedFileName = request.data['file']
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            # Check the file already uploaded.
            dataSet = DataSet.objects.filter(name=uploadedFileName)
            if dataSet:
                return Response({'status': 'error', 'message': 'File already exists'}, status.HTTP_409_CONFLICT)
            # Make other datasets value to false.
            DataSet.objects.update(isDefault=False)
            dataSetObj = DataSet(name=str(uploadedFileName), url='media/'+str(uploadedFileName),
                                 columns='Category', isProcessed=False, fileSize=100, createdBy=1, isActive=True, isDefault=True)

            dataSet_serialiser = DataSetSerializer(data=dataSetObj.__dict__)
            if dataSet_serialiser.is_valid():
                save_result = dataSet_serialiser.save()
            else:
                return Response(dataSet_serialiser.errors, status=status.HTTP_400_BAD_REQUEST)
            file_serializer.save()

            file_path = file_serializer.data['file'].strip("/")
            # Call function for summary
            summary = reportBl.getReport(file_path)                   
            sentimentProduct = reportBl.getSentiment(file_path, "Product Name")                   
            sentimentCategory = reportBl.getSentiment(file_path, "Category")                   
            sentimentSubcategory = reportBl.getSentiment(file_path, "Sub-Category")  
            # Get Charts
            chartCategory = reportBl.getCategoryReport(file_path,"Category").to_dict(orient='records')
            print(chartCategory)
            chartSubCategory = reportBl.getCategoryReport(file_path,"Sub-Category").to_dict(orient='records')
            chartRegion = reportBl.getRegionReport(file_path).to_dict(orient='records')
            chartMonth = reportBl.getMonthReport(file_path)
            print("chartMonth")
            print(chartMonth)
            # Save results#                  
            res = {
                "datasetId":save_result.id,                
                "summary":summary,
                "sentimentProduct":sentimentProduct,
                "sentimentCategory":sentimentCategory,
                "sentimentSubcategory":sentimentSubcategory,
                "chartCategory":chartCategory,
                "chartMonth":chartMonth,
                "chartRegion":chartRegion,
                "chartSubCategory":chartSubCategory
                }              
            
            result_serializer = ResultSerializer(data=res)            
            if result_serializer.is_valid():
                val = result_serializer.save()
                print(val.id)
            else:
                print('not saved to result..')             
                print(result_serializer.errors)
            # return summary
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        data = DataSet.objects.all().order_by('-createdOn')
        serializedData = DataSetSerializer(data, many=True)        
        return Response({'status': 'success', 'data': serializedData.data})

    def delete(self, request, pk, format=None):
        try:
            dataset = DataSet.objects.get(id=pk)
            #  delete from disk
            if os.path.isfile('media/'+dataset.name):
                os.remove('media/'+dataset.name)
            if dataset.id is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                # delete from databse
                dataset.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)          
            
        except DataSet.DoesNotExist:
            dataset = None
        return Response(status=status.HTTP_404_NOT_FOUND)

#     def post(self, request, format=None):
#         # to access files
#         print(request.FILES)
#         # for filename, file in request.FILES.iteritems():
#         #     name = request.FILES[filename].name
#         #     print(name)
#         # to access data
#         print(request.data)
#         # print(request.data)
#         return Response({'received data': request.data})


# class FileUploadView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

    # def put(self, request, filename, format='xlsx'):
    #     file_obj = request.data['file']
    #     file_obj1 = request.FILES['file']
    #     # df = open(file_obj1)
    #     uploaded_file = request.FILES['file']

    #     dir_path = os.path.dirname(os.path.realpath(__file__))
    #     # print(dir_path)
    #     dest_file_path = os.path.join(dir_path, "newfile.xlsx")

    #     data = pd.read_excel(file_obj)
    # print(data)

    # with open(dest_file_path,"wb") as myfile:
    #     for chunk in file_obj.chunks():
    #         myfile.write(chunk)
    #         print("-----------------")

    # data = pd.read_csv(file_obj, error_bad_lines=False, encoding='latin-1')
    # data = pd.read_html(file_obj)
    # book = xlrd.open_workbook(file_contents=uploaded_file)
    # df = pd.read_table(dest_file_path)
    # print(df)
    # wb = xlrd.open_workbook(dest_file_path)
    # sh = wb.sheet_by_index(0)
    # print(sh.cell(0,0).value)

    # f = open(uploaded_file, 'rb')
    # bytes = f.read()
    # f.close()
    # wb = xlrd.open_workbook(file_contents=bytes)
    # print(wb)

    # data = pd.read_html(uploaded_file,  encoding='latin-1')

    # print(data)

    # print(data["Start Date"])

    # wb = xlrd.open_workbook(filename=None, file_contents=uploaded_file.read())

    # try:
    #     fd, tmp = tempfile.mkstemp()
    #     with os.fdopen(fd, 'w') as out:
    #         out.write(uploaded_file.read())
    #     wb = xlrd.open_workbook(tmp)
    # finally:
    #     os.unlink(tmp)  # delete the temp file no matter what

    # data = pd.read_excel(uploaded_file)
    # df_list = pd.read_excel(uploaded_file)
    # df = pd.DataFrame(df_list[0])
    # book = xlrd.open_workbook(file_contents=uploaded_file.read())
    # print("The number of worksheets is", book.nsheets)
    # print("Worksheet name(s):", book.sheet_names())
    # sh = book.sheet_by_index(0)
    # str_text = ''
    # for line in uploaded_file:
    #     str_text = str_text + line.decode()
    #     print(str_text)

    # wb = xlrd.open_workbook(filename=None, file_contents=uploaded_file.read())
    # print(wb)
    # my_saved_file = open(file_obj)  # there you go

    # return Response(status=204)
