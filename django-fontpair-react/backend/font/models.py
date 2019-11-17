from django.db import models

# Create your models here.
class Font(models.Model):
    CATEGORIES =(
        ('d','display'),
        ('h','handwriting'),
        ('m','monospaced')
    )

    WEIGHTS = (
        ('100', 'Thin'),
        ('200', 'Extra Light'),
        ('300', 'Light'),
        ('400', 'Regular'),
        ('500', 'Medium'),
        ('600', 'Semi Bold'),
        ('700', 'Bold'),
        ('800', 'Extra Bold'),
        ('900', 'Black'),
    )

    name = models.TextInput(primary_key=True)
    family = models.TextInput()
    category = models.TextInput(choices=CATEGORIES)
    is_body = models.BooleanField(default=True)
    is_serif = models.BooleanField(default=True)
    is_italic = models.BooleanField(default=False)
    weight = models.PositiveIntegerField(choices=WEIGHTS)
    url = models.URLField()

class Fontpair(models.Model):
    font1 = models.ForeignKey(Font, on_delete=models.CASCADE)
    font2 = models.ForeignKey(Font, on_delete=models.CASCADE)