from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import authentication_classes, permission_classes

from upload.models import DataSet
from reports.models import Result
from reports.serializers import ResultSerializer

@permission_classes((AllowAny, ))
class DefaultDatasetView(APIView):
    def post(self, request, *args, **kwargs):
        datasetId = request.query_params.get('id')

        DataSet.objects.update(isDefault=False)
        DataSet.objects.filter(id=datasetId).update(isDefault=True)
        
        try:
            summary_data = Result.objects.get(datasetId_id= datasetId)
        except:
            return Response({"status": "success", "data": []})    

        result_serializer = ResultSerializer(summary_data)        
        return Response({"status": "success", "data": result_serializer.data})