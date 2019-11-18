from django.db import models
import django.db.models.fields

class Font(models.Model):
    WEIGHTS = (
        ('thin', 'Thin'),
        ('extralight', 'Extra Light'),
        ('light', 'Light'),
        ('regular', 'Regular'),
        ('medium', 'Medium'),
        ('semibold', 'Semi Bold'),
        ('bold', 'Bold'),
        ('extrabold', 'Extra Bold'),
        ('black', 'Black'),
    )

    name = models.CharField(max_length=255, primary_key=True)
    family = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    is_body = models.BooleanField(default=True)
    is_serif = models.BooleanField(default=True)
    is_italic = models.BooleanField(default=False)
    weight = models.CharField(max_length=20, choices=WEIGHTS)
    url = models.URLField()

    def _str_(self):
        # return name
        return '{} {}'.format(self.family, self.weight)

class FontPair(models.Model):
    font1 = models.ForeignKey(Font, related_name='font1', on_delete=models.CASCADE)
    font2 = models.ForeignKey(Font, related_name='font2', on_delete=models.CASCADE)

    def _str_(self):
        return '({}, {})'.format(self.font1, self.font2)

# class FontPair(models.Model):
#   title = models.CharField(max_length=120)
#   description = models.TextField()
#   completed = models.BooleanField(default=False)

#   def _str_(self):
#     return self.title

# class Font(models.Model):
#     name = models.CharField(max_length=100)
#     family = models.TextField()
#     category = models.CharField(max_length=100)
#     image = models.FilePathField(path="/img")