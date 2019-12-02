from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, default=None, primary_key=True)
    class Meta:
        verbose_name_plural = 'Categories'

    def __str_(self):
        return '{}'.format(self.name)