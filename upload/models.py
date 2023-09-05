from django.db import models


class File(models.Model):
    file = models.FileField(blank=False, null=False)
    remark = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

class DataSet(models.Model):
    name = models.CharField(max_length=50, null=False)
    url = models.CharField(max_length=30, null=False)
    columns = models.CharField(max_length=200, null=True)
    isProcessed = models.BooleanField()    
    fileSize = models.PositiveIntegerField()
    createdBy = models.PositiveIntegerField()
    createdOn = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField()  
    isDefault = models.BooleanField(null=True)  

    # def __str__(self):
    #     return self.name
