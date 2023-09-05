from django.contrib.postgres.fields import JSONField
from django.db import models
from upload.models import DataSet

class Result(models.Model):
    datasetId = models.ForeignKey(DataSet, on_delete=models.CASCADE)
    summary = JSONField(null=True)
    sentimentProduct = JSONField(null=True)
    sentimentCategory = JSONField(null=True)
    sentimentSubcategory = JSONField(null=True)
    chartCategory = JSONField(null=True)
    chartSubCategory = JSONField(null=True)
    chartMonth=JSONField(null=True)
    chartRegion=JSONField(null=True)
    
