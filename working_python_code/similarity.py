from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

def calculate_cosine_similarity_matrix(embeddings, ids):
    '''Calculates a cosine similarity matrix from the embeddings'''
    similarity_matrix = pd.DataFrame(cosine_similarity(X=embeddings),index=ids)

    return similarity_matrix

def get_n_recommended_fonts(similarity_matrix, font_dict, font, n):
        # Get the similarity scores for the specified font

        # Get keys from dictionary and the corresponding id/index
        keys = font_dict.index.tolist()
        font_id = keys.index(font)
        font_row = font_dict.iloc[font_id]

        similar_items = pd.DataFrame(similarity_matrix.iloc[font_id])
        similar_items.columns = ['similarity_score']

        # Create separate dataframes for similar and dissimilar items
        similar = similar_items.sort_values('similarity_score', ascending=False)
        dissimilar = similar_items.sort_values('similarity_score', ascending=True)

        # Get the first n elements of both similar and dissimilar
        # n_similar = []
        # for i in range(0,n*2):
        #     if similar_items[i]['similarity_score'] != 1:
        #         n_similar.append(similar_items[i])

        # Get names of indexes for which column Age has value 30
        # print(similar[similar==1])
        # print(similar.head())
        too_similar = similar[ similar['similarity_score'] > 0.99 ].index
        # print("too similar:\n",indexNames)

        # Delete these row indexes from dataFrame
        similar.drop(too_similar, inplace=True)

        n_similar = similar.head(n)
        # n_dissimilar = dissimilar.head(n*2)
        xx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        n_dissimilar = dissimilar
        n_dissimilar.drop(xx,inplace=True)
        print(n_similar)
        print("n_dissimilar:\n",n_dissimilar)

        # Get rows for all recommended fonts
        idx_s = n_similar.index.tolist()
        idx_d = n_dissimilar.index.tolist()
        print(idx_s," ",idx_d)

        rows_s = []
        rows_d = []

        for i in range(0,n):
            curr_idx_s = idx_s[i]
            curr_idx_d = idx_d[i]
            rows_s.append(font_dict.iloc[curr_idx_s])
            rows_d.append(font_dict.iloc[curr_idx_d])

        # Reset indices so the original indices can be a separate column
        n_similar.reset_index(inplace=True)
        n_dissimilar.reset_index(inplace=True)

        # Redefine dataframes
        n_similar = n_similar.rename(index=str, columns={"index": "item_id"})
        n_dissimilar = n_dissimilar.rename(index=str, columns={"index": "item_id"})

        # Return rows, n_similar, n_dissimilar
        # return rows_s, rows_d
        return rows_s[0:n][0], rows_d[0:n][0], n_similar, n_dissimilar, rows_s, rows_d

def calculate_contrast_similarity(embeddings):
    # Take dot product of embeddings

# def activation_function(a,b,n):
    # a is a vector a = (a1, a2, ... an), b is a vector b = (b1, b2, ... bn)
    # n is the dimension of the vectors

    # Contrast similarity = -N*P
    P = 0 # P = sum(a*b) from i:n when [a*b > 0]
    N = 0 # N = sum(a*b) from i:n when [a*b < 0]

    for i in range(0,n):
        product = a[i]*b[i]
        if product > 0:
            P = P + product
        else: # product < 0
            N = N + product

    return -N*P