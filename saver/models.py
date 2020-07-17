from django.db import models
from .utils import custom_upload_path


class Pack(models.Model):
    '''Represents a single file'''
    f = models.FileField(upload_to=custom_upload_path)
    hash_name = models.CharField(max_length=64, null=True, blank=True, db_index=True)

    def __str__(self):
        return f'<Pack {self.hash_name}>'
