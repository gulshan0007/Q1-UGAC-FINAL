from django.db import models

# Create your models here.
class FilesAdmin(models.Model):
    adminupload=models.FileField(upload_to='media')
    title=models.CharField(max_length=50)

    def _str_(self):
        return self.title
