from django.db import models

# Create your models here.
class Family(models.Model):
    name = models.CharField(max_length=255, default=None, primary_key=True)
    url = models.URLField()

    class Meta:
        verbose_name_plural = 'Families'

    def __str_(self):
        return '{}'.format(self.name)