from django.db import models
import joblib
import numpy as np
from families import models as models_fam
from categories import models as models_cat

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
    # family = models.ForeignKey(Family, 'related_name'='family', on_delete=models.CASCADE)
    category = models.CharField(max_length=255, default=None)
    # category = models.ManyToManyField('FontCategory', related_name='name')
    # category = models.ForeignKey(Category, 'related_name'='category', on_delete=models.CASCADE)
    is_body = models.BooleanField(default=True)
    is_serif = models.BooleanField(default=True)
    is_italic = models.BooleanField(default=False)
    # weight = models.ManyToManyField('FontWeight', 'related_name=name')
    weight = models.CharField(max_length=20, choices=WEIGHTS, default='regular')
    url = models.URLField()

    class Meta:
        ordering = ['name']

    def __str_(self):
        # return name
        return '{} {}'.format(self.family, self.category)

    def get_recommendations(font_obj,fonts,vectors,knn,num_recs):
        # Load pickle files
        # fonts = joblib.load('fonts.pkl')
        # vectors = joblib.load('vectors.pkl')
        # knn = joblib.load('knn.pkl')
        # print(font_obj)
        # font = font_obj.name
        # print(font)
        # print(fonts.head())
        # print(fonts.index)
        # print('original keys: ',fonts.keys())
        fonts.set_index('name',drop=True, append=False,inplace=True)
        # print(fonts)
        # print('new indices', fonts.index)
        # print('new keys: ', fonts.keys())

        # Get font object and find corresponding vector
        font = fonts.loc[font_obj.name]
        idx = font['idx']
        choice = vectors[idx]
        # print(fonts.iloc[0])
        # print(fonts.loc['ABeeZee 400'])
        # print('font: ',font)
        # print('font type: ',type(font))
        # print(fonts.head())
        # choice = fonts.loc[font]
        # print('choice: ',choice)

        # Get nearest-furthest vectors for specified font
        print('~~~~~~~~~~~ attempting knn ~~~~~~~~~~~')
        distances,indices = knn.kneighbors([choice])
        # print('distances: ',distances)
        # print('indices: ',indices)
        sim_vectors = indices[0]
        diff_vectors = np.flipud(sim_vectors)

        # Use recommended vectors to find corresponding font objects
        similar = []
        dissimilar = []
        for i in range(0,num_recs):
            curr_sim = sim_vectors[i]
            curr_dis = diff_vectors[i]

            print(fonts.iloc[curr_sim].name)
            similar.append(fonts.iloc[curr_sim].name)
            dissimilar.append(fonts.iloc[curr_dis].name)

        # Add both similar and dissimilar fonts to final recommendation list
        print('~~~~~~~~~~~ getting recs ~~~~~~~~~~~')

        # Find corresponding font models for each entry in recommendation list
        print('similar: ',similar)
        # print('similar[0]: ',similar[0])
        # sim_names = similar['name'].tolist()
        # diff_names = dissimilar['name'].tolist()
        print('~~~~~~~~~~~ getting rec models ~~~~~~~~~~~')
        recs_sim = []
        recs_diff = []

        for i in range(0,num_recs):
            # print('similar at index ',i,': ',similar[i])
            # print(similar[i].index)
            # print(similar[i].keys())
        # for ns in sim_names:
            ns = similar[i]
            print('ns: ',ns)
            curr = Font.objects.get(pk=ns)
            recs_sim.append(curr)

            nd = dissimilar[i]
            print('nd: ',nd)
            curr = Font.objects.get(pk=nd)
            recs_diff.append(curr)

        # for nd in diff_names:
        #     curr = Font.objects.get(nd)
        #     recs_diff.append(curr)

        # return full_recs, similar, dissimilar
        return recs_sim, recs_diff

class FontPair(models.Model):
    font1 = models.ForeignKey(Font, related_name='font1', on_delete=models.CASCADE)
    font2 = models.ForeignKey(Font, related_name='font2', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Pairings"

    def __str_(self):
        return '({}, {})'.format(self.font1, self.font2)

class Weight(models.Model):
    weight = models.IntegerField(default=None, unique=True)
    string = models.CharField(max_length=255, default=None, primary_key=True)

    class Meta:
        ordering = ['weight']

    def __str_(self):
        return '{} ({})'.format(self.string, self.weight)