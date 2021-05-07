from django.db import models

# Create your models here.

class Audio1doc(models.Model):
    Name = models.CharField(max_length=150)
    Action = models.FileField(upload_to='cloud/attachments/')
 
    def __str__(self):
        return self.Name