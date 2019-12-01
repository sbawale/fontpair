import os
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from preprocess_data_gf import *

def get_font_combinations(font,fonts,vectors,knn,num_recs):
    # Get font object and find corresponding vector
    font_obj = fonts.loc[font]
    idx = font_obj['idx']
    choice = vectors[idx]

    # Get nearest-furthest vectors for specified font
    distances,indices = knn.kneighbors([choice])
    sim_vectors = indices[0]
    diff_vectors = np.flipud(sim_vectors)

    # Use recommended vectors to find corresponding font objects
    similar = []
    dissimilar = []
    for i in range(0,num_recs):
        curr_sim = sim_vectors[i]
        curr_dis = diff_vectors[i]

        similar.append(fonts.iloc[curr_sim])
        dissimilar.append(fonts.iloc[curr_dis])

    # Add both similar and dissimilar fonts to final recommendation list
    full_recs = similar
    full_recs.append(dissimilar)

    return full_recs, similar, dissimilar

def build_recommender():
    # Get preprocessed font data
    fonts = preprocess_data_gf()

    # One-hot encode fonts manually
    ohe_fonts = pd.concat(
        [pd.get_dummies(fonts[['family']]),
        pd.get_dummies(fonts[['category']]),
        pd.get_dummies(fonts[['weight']]),
        fonts[['is_body']],
        fonts[['is_serif']],
        fonts['is_italic']],
        axis=1)

    # Convert one-hot encoded fonts to numeric vectors
    vectors = ohe_fonts.astype(float).to_numpy()

    # Build KNN model
    knn = NearestNeighbors(n_neighbors=len(vectors), metric='euclidean', algorithm='auto').fit(vectors)

    return fonts, vectors, knn

################# TESTING ################

fonts, vectors, knn = build_recommender()

# Feed to KNN algorithm
font_name = 'Yellowtail'
k = 5
full_recs,sim,dis = get_font_combinations(font_name,fonts,vectors,knn,k)
print(full_recs)
# print('sim:\n',sim)
# print('\ndis:\n',dis)