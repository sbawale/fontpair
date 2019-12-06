from django.db import models
from categories import models as cm
# from import_export import fields, resources
# from import_export.widgets import ForeignKeyWidget

# Create your models here.
class Family(models.Model):
    name = models.CharField(max_length=255, default=None, primary_key=True)
    category = models.ForeignKey(cm.Category, default=None, on_delete=models.CASCADE)
    url = models.URLField()

    class Meta:
        verbose_name_plural = 'Families'

    def __str_(self):
        return '{}'.format(self.name)