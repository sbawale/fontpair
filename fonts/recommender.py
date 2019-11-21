import os
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from .working_python_code import preprocess_data_gf, helper_functions, similarity
from .models import *

# ********************** KNN rec system **********************

def build_knn_recommender():
    # Preprocess data
    fonts = preprocess_data_gf()

    # One-hot encode fonts for scaling
    ohe_fonts = pd.concat(
        # [fonts["category"].str.get_dummies(sep=","),
        [pd.get_dummies(fonts[["category"]]),
        pd.get_dummies(fonts[["weight"]]),
        fonts[["is_body"]],
        fonts[["is_serif"]],
        fonts["is_italic"]],
        axis=1)

    # Scale fonts
    min_max_scaler = MinMaxScaler()
    font_vectors = min_max_scaler.fit_transform(ohe_fonts)

    # Build KNN model using font vectors
    knn_model = NearestNeighbors(n_neighbors=6, metric='cosine', algorithm='auto').fit(font_vectors)
    distances, indices = knn_model.kneighbors(font_vectors)

# ********************** Embedding rec system **********************

def embedding_recommender():
    # Preprocess data, then get font dictionary with TF-IDF vectors
    test = preprocess_data_gf()
    vectors, font_dict = get_font_vectors(test,0) # this is a sparse CSR matrix
    ids = font_dict['id'].tolist()
    # Or use this method? - no, probably still need AE but this will do for now
    # dense = vectors.toarray()
    dense = vectors.todense()
    # print("dense\n",dense)
    # print(dense.shape)
    embeddings = pd.DataFrame(dense)
    # embeddings.to_csv(r"testdense.csv", index = None, header=True)
    # print(csr_matrix(dense))

    # Create similarity matrix, test predictive function
    print("calculating cosine similarity matrix...")
    sim_matrix = calculate_cosine_similarity_matrix(embeddings, ids)
    # print(sim_matrix.columns)
    print("cosine similarity matrix created!\ntesting recommender function...")
    similar, dissimilar = get_n_recommended_fonts(sim_matrix, font_dict, 'Open Sans 400', 5)
    print("similar fonts:\n",similar)
    print("\ndissimilar fonts:\n",dissimilar)

# ********************** Helper Functions **********************

def build_recommender(choice):
    return something

def build_similarity_matrix():
    return something

def get_font_combinations(fonts,indices,font,num_recs): # FIX ME SO I CAN TAKE FONT NAME
    pairings = []
    # Get font name/index pair
    temp = fonts.iloc[0:num_recs-1]
    for t in temp:
        print(temp[t]['name'])
        pairings.append(temp[t])
    f = fonts.loc[font]
    # f = font
    # Get recommended fonts
    for i in indices[f][0:num_recs-1]:
        print(fonts.iloc[i]["name"])
        print(fonts.iloc[i]["url"])

    return pairings