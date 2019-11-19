import os
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from ./data import preprocess_data_gf, helper_functions, similarity
from .models import *
# from preprocess_data_gf import *
# from helper_functions import *
# from similarity import *

# ********************** KNN rec system **********************

# Preprocess data
# fonts = preprocess_data_gf()

# Get font objects
fonts = Font.objects.all()

for f in font:


# One-hot encode fonts for scaling
ohe_fonts = pd.concat(
    [fonts["category"].str.get_dummies(sep=","),
    pd.get_dummies(fonts[["weight"]]),
    fonts[["is_body"]],
    fonts[["is_serif"]],
    fonts["is_italic"]],
    axis=1)

min_max_scaler = MinMaxScaler()
font_vectors = min_max_scaler.fit_transform(ohe_fonts)

# Build KNN model using font vectors
nbrs = NearestNeighbors(n_neighbors=6, metric='cosine', algorithm='brute').fit(ohe_fonts)
distances, indices = nbrs.kneighbors(ohe_fonts)
# choice = fonts.loc['Yellowtail']
# choice = 'Yellowtail'
# get_font_combinations(fonts,indices,choice,5)


# ********************** Embedding rec system **********************

# # Preprocess data, then get font dictionary with TF-IDF vectors
# test = preprocess_data_gf()
# vectors, font_dict = get_font_vectors(test,0) # this is a sparse CSR matrix
# ids = font_dict['id'].tolist()
# # Or use this method? - no, probably still need AE but this will do for now
# # dense = vectors.toarray()
# dense = vectors.todense()
# # print("dense\n",dense)
# # print(dense.shape)
# embeddings = pd.DataFrame(dense)
# # embeddings.to_csv(r"testdense.csv", index = None, header=True)
# # print(csr_matrix(dense))

# # Create similarity matrix, test predictive function
# print("calculating cosine similarity matrix...")
# sim_matrix = calculate_cosine_similarity_matrix(embeddings, ids)
# # print(sim_matrix.columns)
# print("cosine similarity matrix created!\ntesting recommender function...")
# similar, dissimilar = get_n_recommended_fonts(sim_matrix, font_dict, 'Open Sans 400', 5)
# print("similar fonts:\n",similar)
# print("\ndissimilar fonts:\n",dissimilar)