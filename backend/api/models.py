from django.db import models

# Create your models here.
class Dataset(models.Model):
    file=models.FileField(upload_to='uploads/')
    uploaded_at=models.DateTimeField(auto_now_add=True)
    total_count= models.IntegerField()
    avg_flowrate= models.FloatField()
    avg_pressure= models.FloatField()
    avg_temperature= models.FloatField()
    type_distriction = models.JSONField()
    class Meta:
        ordering = ['-uploaded_at']