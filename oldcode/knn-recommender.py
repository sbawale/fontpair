import os
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from preprocess_data_gf import *
from helper_functions import *

# def build_knn_model():

# Preprocess data, split into train/test/val sets
fonts = filter_data_gf()
train_set, test_set, val_set = split_train_test_val(fonts,0.8)


ohe_fonts = pd.concat(
    [fonts["category"].str.get_dummies(sep=","),
    pd.get_dummies(fonts[["weight"]]),
    fonts[["is_body"]],
    fonts[["is_serif"]],
    fonts["is_italic"]],
    axis=1)

print(ohe_fonts)
print(ohe_fonts.columns)

min_max_scaler = MinMaxScaler()
font_vectors = min_max_scaler.fit_transform(ohe_fonts)
print(font_vectors)
print(font_vectors.shape)

nbrs = NearestNeighbors(n_neighbors=6, metric='cosine', algorithm='brute').fit(ohe_fonts)
distances, indices = nbrs.kneighbors(ohe_fonts)
print(distances)
print(indices)

for id in indices[9][1:5]:
    print(fonts.iloc[id]["name"])

def get_font_combinations(fonts,indices,font,num_recs):
    # Get font name/index pair
    f = fonts.loc['font']

    # Get recommended fonts
    for i in indices[f][1:num_recs]:
        print(fonts.iloc[i]["name"])

# print_similar_animes(query="Naruto")

# def get_index_from_name(name):
#     return anime[anime["name"]==name].index.tolist()[0]

# def get_id_from_partial_name(partial):
#     all_anime_names = list(anime.name.values)
#     for name in all_anime_names:
#         if partial in name:
#             print(name,all_anime_names.index(name))

# def print_similar_animes(query=None,id=None):
#     if id:
#         for id in indices[id][1:]:
#             print(fonts.ix[id]["name"])
#     if query:
#         found_id = get_index_from_name(query)
#         for id in indices[found_id][1:]:
#             print(fonts.ix[id]["name"])

# pleasework = [fonts[['category', 'weight']]]
# print(pleasework)
# ohe_fw = pd.get_dummies(pleasework)
# print(ohe)

# ohe_cat = pd.get_dummies(fonts['category'])
# ohe_body = pd.get_dummies(fonts['is_body'])
# ohe_serif = pd.get_dummies(fonts['is_serif'])
# ohe_italic = pd.get_dummies(fonts['is_italic'])
# ohe_weight = pd.get_dummies(fonts['weight'])

# ohe_fonts = pd.concat(
#     ohe_cat,
#     ohe_body,
#     ohe_serif,
#     ohe_italic,
#     ohe_weight)
# ohe_fonts = ohe_cat.append(ohe_weight)
# print(ohe_fonts)

# vectors = pd.concat(
#     fonts['name'].tolist(),
#     ohe_fonts,
#     fonts['is_body'],
#     fonts['is_serif'],
#     fonts['is_italic'],
#     fonts['weight'])
# print(vectors.head())

# font_dict = pd.concat(ohe_fw)
# font_dict.insert(1, 'is_body', fonts['is_body'])
# font_dict.insert(2, 'is_serif', fonts['is_serif'])
# font_dict.insert(3, 'is_italic', fonts['is_italic'])
# font_dict.insert(4, 'weight', ohe_weight)
# font_dict.insert(0, 'id', font_dict.index.tolist())
# font_dict.set_index('name', drop=True, append=False, inplace=True, verify_integrity=False)
# print(font_dict.head())
# sub = test[['category','is_body','is_serif','is_italic','weight']]
# print(sub.columns)

# ohe = OneHotEncoder()
# x = ohe.fit(sub['category'])
# print(x)


# enc = OneHotEncoder(categorical_features = [0])
# enc.fit_transform(sub)
# print(sub)

# pd.get_dummies(sub, columns=["category"]).head()

# min_max_scaler = MinMaxScaler()
# anime_features = min_max_scaler.fit_transform(sub)
# print(anime_features)


# nbrs = NearestNeighbors(n_neighbors=6, algorithm='ball_tree').fit(sub)
# distances, indices = nbrs.kneighbors(sub)
# print(distances)
# print(indices)


# def one_hot_encode_fonts(fonts):
#     vector = []
#     categories = fonts['category']


# def help:
#     #make an object for the NearestNeighbors Class.
#     model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
#     # fit the dataset
#     model_knn.fit(train_set)


#     # example recommendation
#     my_favorite = 'Iron Man'

#     make_recommendation(
#         model_knn=model_knn,
#         data=train_set,
#         mapper=movie_to_idx,
#         fav_movie=my_favorite,
#         n_recommendations=10
#         )

# def make_recommendation(model_knn, data, mapper, fav_movie, n_recommendations):

#     # fit
#     model_knn.fit(data)
#     # get input movie index
#     print('You have input movie:', fav_movie)
#     idx = fuzzy_matching(mapper, fav_movie, verbose=True)

#     print('Recommendation system start to make inference')
#     print('......\n')
#     distances, indices = model_knn.kneighbors(data[idx], n_neighbors=n_recommendations+1)

#     raw_recommends = \
#         sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])[:0:-1]
#     # get reverse mapper
#     reverse_mapper = {v: k for k, v in mapper.items()}
#     # print recommendations
#     print('Recommendations for {}:'.format(fav_movie))
#     for i, (idx, dist) in enumerate(raw_recommends):
#         print('{0}: {1}, with distance of {2}'.format(i+1, reverse_mapper[idx], dist))