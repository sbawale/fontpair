import joblib
import numpy as np
from django.db import models
from families import models as fm
from categories import models as cm

# Create your models here.
class Font(models.Model):
    name = models.CharField(max_length=255, default=None, primary_key=True)
    family = models.ForeignKey(fm.Family, on_delete=models.CASCADE)
    category = models.ForeignKey(cm.Category, on_delete=models.CASCADE)
    is_body = models.BooleanField(default=True)
    is_serif = models.BooleanField(default=True)
    is_italic = models.BooleanField(default=False)
    weight_num = models.IntegerField(default=400)
    weight_str = models.CharField(max_length=20, default='regular')

    class Meta:
        ordering = ['name']

    def __str_(self):
        return name

    def get_random(self, items=1):
        if isinstance(items, int):
            return self.model.objects.order_by('?')[:items]
        return self.all()

    def get_recommendations(font_obj,fonts,vectors,knn,num_recs):
        # Get font object and find corresponding vector
        fonts.set_index('name',drop=True, append=False,inplace=True)
        font = fonts.loc[font_obj.name]
        idx = font['idx']
        choice = vectors[idx]

        # Get nearest-furthest vectors for specified font
        distances,indices = knn.kneighbors([choice])
        sim_vectors = indices[0]
        diff_vectors = np.flipud(sim_vectors)

        # Use recommended vectors to find corresponding font objects
        similar = []
        dissimilar = []
        for i in range(0,num_recs):
            curr_sim = sim_vectors[i+1] # exclude self from recommendation list
            curr_dis = diff_vectors[i]

            print(fonts.iloc[curr_sim].name)
            similar.append(fonts.iloc[curr_sim].name)
            dissimilar.append(fonts.iloc[curr_dis].name)

        # Find corresponding font models for each entry in recommendation list
        recs_sim = []
        recs_diff = []

        for i in range(0,num_recs):
            ns = similar[i]
            curr = Font.objects.get(pk=ns)
            recs_sim.append(curr)

            nd = dissimilar[i]
            curr = Font.objects.get(pk=nd)
            recs_diff.append(curr)

        # return full_recs, similar, dissimilar
        return recs_sim, recs_diff