from django.db import models

# Create your models here.
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

    name = models.CharField(max_length=255, default=None, primary_key=True)
    family = models.CharField(max_length=255, default=None)
    category = models.CharField(max_length=255, default=None)
    # category = models.ManyToManyField('FontCategory', related_name='name')
    is_body = models.BooleanField(default=True)
    is_serif = models.BooleanField(default=True)
    is_italic = models.BooleanField(default=False)
    weight = models.CharField(max_length=20, choices=WEIGHTS, default='regular')
    url = models.URLField()

    def __str_(self):
        # return name
        return '{} {}'.format(self.family, self.category)

class FontPair(models.Model):
    font1 = models.ForeignKey(Font, related_name='font1', on_delete=models.CASCADE)
    font2 = models.ForeignKey(Font, related_name='font2', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Pairings"

    def _str_(self):
        return '({}, {})'.format(self.font1, self.font2)

class Weight(models.Model):
    weight = models.IntegerField(default=None, unique=True)
    string = models.CharField(max_length=255, default=None, primary_key=True)
    def __str_(self):
        return '{} ({})'.format(self.string, self.weight)