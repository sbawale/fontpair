import pandas as pd
import numpy as np
from preprocess_data_gf import *
from helper_functions import *
from similarity import *

# Preprocess data, split into train/test/val sets
test = preprocess_data_gf()
print(test.head(10))
train_set, test_set, val_set = split_train_test_val(test,0.8)
# print(train_set)
# print(test_set)
# print(val_set)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(test)
# test.to_csv(r"testgf.csv", index = None, header=True)

# Get font dictionary with TF-IDF vectors
# vectors = get_font_vectors(test,0)
vectors, font_dict = get_font_vectors(test,0) # this is a sparse CSR matrix
print(font_dict.head())
print(vectors[0:4])
ids = font_dict['id'].tolist()
# print(ids[0:4])
# print("vectors\n",vectors)
# print(vectors.shape)
# pd.DataFrame(vectors).to_csv(r"testvectors.csv", index = None, header=True)
# Compress vectors by feeding them to autoencoder
# ae = AutoEncoder(vectors)
# print(issparse(vectors))

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