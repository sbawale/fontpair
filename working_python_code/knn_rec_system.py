import os, webbrowser
import pandas as pd
from sklearn import preprocessing
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial import distance
from preprocess_data_gf import *
from helper_functions import *
from similarity import *
from knn_scratch import *

def get_knn_neighbors(dictionary, font_name, k):
    distances = []
    font_vector = dictionary[font_name] # vector of font to match
    # print('font_vector: ',font_vector)

    for entry in dictionary:
        current_vector = dictionary[entry] # get vector of current font
        # print('current_vector: ',current_vector)
        dist = distance.euclidean(font_vector,current_vector)
        distances.append([entry,dist])

    similar = sorted(distances)
    dissimilar = sorted(distances, reverse=True)
    # print('similar: ',similar)

    # Return k most similar fonts (excluding self) and k most dissimilar fonts
    return similar[1:k+1],dissimilar[0:k]

################## OHE VERSION ################

def get_ohe_vectors(fonts):
    ohe_fonts = pd.concat(
        [pd.get_dummies(fonts[['family']]),
        pd.get_dummies(fonts[['category']]),
        pd.get_dummies(fonts[['weight']]),
        fonts[['is_body']],
        fonts[['is_serif']],
        fonts['is_italic']],
        axis=1)
    # print('ohe_fonts:\n',ohe_fonts)
    # print('\nohe_fonts cols: ',ohe_fonts.columns)
    # pd.DataFrame(ohe_fonts).to_csv(r'ohe.csv',header=True)

    # Convert one-hot encoded fonts to numeric vectors
    vectors = ohe_fonts.astype(float).to_numpy()
    # print(font_vectors)

    # # Testing euclidean distance
    # print('testing euclidean distance...\n')
    # x = vectors[1002]
    # y = vectors[99]
    # dist = distance.euclidean(x,y)
    # print('x:',x)
    # print('y:',y)
    # print('dist:',dist)

    # Create dictionary of font name: vector
    ohe_dict = {}
    names = ohe_fonts.index.tolist()

    for i in range(0,len(vectors)):
        name = names[i]
        ohe_dict[name] = vectors[i]

    return vectors, ohe_dict


################# TFIDF VERSION ################

def get_font_vectors_tfidf(fonts, include_family):
    # Convert all features (weight, category, etc.) to single bag of words
    bags_of_words = []

    for font in fonts.itertuples(index=False,name=None):
        if include_family:
            family = font[1].split()
            no_digits = ''.join(filter(lambda x: not x.isdigit(), family))
            curr_bag = str(no_digits) + ' ' + str(font[2])
        else:
            curr_bag = str(font[2])

        # Get body value
        if font[3] == 1: body = ' body'
        else: body = ' heading'

        # Get serif value
        if font[4] == 1: serif = ' serif'
        else: serif = ' sans-serif'

        # Get italic value
        if font[5] == 1: italic = ' italic'
        else: italic = ' roman'

        # Add the current bag to the list of all bags
        curr_bag = curr_bag + body + serif + italic + ' ' + str(font[6])
        bags_of_words.append(curr_bag)

    # Convert bags of words to TF-IDF vectors
    # print('\nattempting to create vectors...\n')
    tfidf = TfidfVectorizer(ngram_range=(1, 1), min_df=0.0001)
    tfidf_matrix = tfidf.fit_transform(bags_of_words)
    vectors = tfidf_matrix.todense()
    # print('vectors:\n',vectors)
    # print(type(vectors))
    # print(vectors[10])
    # print('successfully vectorized fonts!')

    # Create dictionary of font name: vector
    tfidf_dict = {}
    names = fonts.index.tolist()

    for i in range(0,len(names)):
        name = names[i]
        tfidf_dict[name] = vectors[i]

    # Create new dataframe with 4 columns: font name, original bag of words, vector, id
    # print("\ncreating new dataframe...\n")
    # font_dict = pd.DataFrame()
    # font_dict['name'] = fonts.index.tolist()
    # font_dict['bag_of_words'] = bags_of_words
    # font_dict['vector'] = vectors
    # font_dict['id'] = font_dict.index.tolist()

    # font_dict.set_index(font_dict['name'], drop=True, append=False, inplace=True, verify_integrity=False)
    # font_dict.to_csv('vectortest.csv')
    # print("\ndataframe created!\n")

    # return vectors, font_dict.to_dict()
    return vectors, tfidf_dict

################# TESTING ################

# Get preprocessed font data
fonts = preprocess_data_gf()

print('testing knn algorithm...\n')
font_name = 'Yellowtail'
k = 10
print('font: ',font_name,'\nk: ',k)

# Feed to KNN algorithm: OHE
print('\n******* ohe version *******\n')
ohe_vectors, ohe_dict = get_ohe_vectors(fonts)
# print(type(ohe_vectors))
# print(type(ohe_dict))
s,d = get_knn_neighbors(ohe_dict, font_name, k)
# print('ohe s:\n',s)
# print('\nohe d:\n',d)

# Feed to KNN algorithm: TF-IDF
print('\n******* tf-idf version *******\n')
tfidf_vectors, tfidf_dict = get_font_vectors_tfidf(fonts, 0)
# print(type(tfidf_vectors))
# print(type(tfidf_dict))
# print(tfidf_dict)
s,d = get_knn_neighbors(tfidf_dict, font_name, k)
# print('tfidf s:\n',s)
# print('\ntfidf d:\n',d)

# Preprocess data
fonts = preprocess_data_gf()
# print('fonts head: ',fonts.head())
# print('feature cols only: ', fonts[['category','is_body','is_italic','is_serif','weight']].head())
# print('keys: ', fonts.keys())
# print('find Yellowtail: ', fonts.loc['Yellowtail'])
why = np.vectorize(fonts)
print('help\n',why)
print(why[0])
# One-hot encode fonts for scaling
ohe_fonts = pd.concat(
    [pd.get_dummies(fonts[['family']]),
    pd.get_dummies(fonts[['category']]),
    pd.get_dummies(fonts[['weight']]),
    fonts[['is_body']],
    fonts[['is_serif']],
    fonts['is_italic']],
    axis=1)
# print('ohe_fonts:\n',ohe_fonts)
# print('\nohe_fonts cols: ',ohe_fonts.columns)
# pd.DataFrame(ohe_fonts).to_csv(r'ohe.csv',header=True)
font_vectors = ohe_fonts
print(font_vectors.keys())
ttt = distance.euclidean(font_vectors[0],font_vectors[1])

families = fonts['family'].unique()
categories = ['display','handwriting','monospace','serif','sans-serif']
font_weights = ['thin','extralight','light','regular','medium','semibold','bold','extrabold','black']

le_cat = LabelEncoder()
le_weight = LabelEncoder()
le_family = LabelEncoder()

le_cat.fit(categories)
le_weight.fit(font_weights)
le_family.fit(families)

copy = fonts

copy['category'] = le_cat.transform(copy['category'])
copy['weight'] = le_weight.transform(copy['weight'])
copy['family'] = le_family.transform(copy['family'])
print(copy)
# scaler = MinMaxScaler()
scaler = StandardScaler()
# scaler.fit_transform(copy[['family','category','weight']])
# scaler.fit_transform(copy['family'])
# scaler.fit_transform(copy['category'])
# scaler.fit_transform(copy['weight'])
# copy['category'] = preprocessing.normalize([copy['category']])
print(copy)

tfidf = TfidfVectorizer(ngram_range=(1, 1), min_df=0.0001)
tfidf_matrix = tfidf.fit_transform(fonts)
print('whole matrix:\n',tfidf_matrix)
# ttt = tfidf_matrix[0] - tfidf_matrix[1]
ttt = distance.euclidean(tfidf_matrix[0],tfidf_matrix[1])
print('subtraction test:\n',ttt)
# print("cat: ",cat)
# print('weight:',wt)
# print('fam:',fam)
# print(cat.shape)
# print(np.fliplr(cat).shape)

# cat_df = pd.DataFrame(data=cat,columns=['category'])
# wt_df = pd.DataFrame(data=cat,columns=['weight'])
# fam_df = pd.DataFrame(data=cat,columns=['family'])

# cat_df.reset_index(drop=True, inplace=True)
# wt_df.reset_index(drop=True, inplace=True)
# fam_df.reset_index(drop=True, inplace=True)

# # print('\ncat_df:\n',cat_df)

# temp1 = fonts[['is_body','is_serif','is_italic']]#.reset_index(drop=True, inplace=True)
# temp1 = temp1.reset_index(drop=True, inplace=True)
# # print(temp1)
# temp1 = pd.concat(
#     [fonts['is_body'],
#     fonts['is_serif'],
#     fonts['is_italic']],
#     axis=1)
# temp1 = temp1.reset_index(drop=True, inplace=True)
# temp2 = pd.concat([cat_df,wt_df,fam_df],axis=1)
# # print('\ntemp1:\n',temp1)
# # print('\ntemp2:\n',temp2)
# temp = pd.concat(
#     [temp1,
#     temp2],
#     axis=1)
# # print('temp:',temp)
# scaler = MinMaxScaler()
# scaler.fit_transform(temp)
# print('temp:',temp)
# print(cat.type)
# Scale one-hot encoded fonts
# min_max_scaler = MinMaxScaler()
# font_vectors = min_max_scaler.fit_transform(ohe_fonts)
# print('\nfont_vectors\n',font_vectors)
# pd.DataFrame(font_vectors).to_csv(r'vectors.csv', header=True)
# print(font_vectors.shape)

# Build KNN model using font vectors
# nbrs = NearestNeighbors(n_neighbors=200, metric='cosine', algorithm='auto').fit(font_vectors)
# distances, indices = nbrs.kneighbors(font_vectors)
nbrs = NearestNeighbors(n_neighbors=10, metric='euclidean', algorithm='auto').fit(font_vectors)
distances, indices = nbrs.kneighbors(font_vectors)
# print('\nknn model:\n',nbrs)
# print('\ndistances:\n',distances)
# print('\nindices:\n',indices)

# ************* Test 1 *************
choice = 'Open Sans 400'
# get_font_combinations(fonts,nbrs,choice,5)
full_recs = get_font_combinations(choice,fonts,font_vectors,nbrs,10)
# print(full_recs)
full_recs_df = pd.DataFrame(full_recs)
full_recs_df.to_csv(r'open_sans_k6.csv', index=None, header=True)
# print('\nrecommendations:\n',full_recs)

print('\nNow testing knn from scratch...\n')
# Index: 1878
# print(font_vectors.head())
# print(font_vectors.keys())
# print(font_vectors.index)
# font_vectors = font_vectors.reset_index()
# print(font_vectors.keys())
# print(font_vectors['Abhaya Libre 500'])

# neighbors = get_neighbors(font_vectors, font_vectors.loc[choice], 10)
# print("\noriginal: \n",font_vectors.loc[choice])
# print("neighbors:")
# for neighbor in neighbors:
#     print(neighbor)
print(font_vectors.keys())
similar,dissimilar = get_k_neighbors(font_vectors, choice, 6, 10)
print(similar)
print(dissimilar)

vecs, font_dict = get_font_vectors_tfidf(fonts, 0)
print(vecs[0])
print(font_dict.keys())
print(font_dict['vector'].shape)
x = font_dict.loc['ABeeZee 400']
print(x)

# ************* Test 2 *************
# current = font_vectors[5]
# # print('\ncurrent:\n',current)
# # print('\nreshaped current:\n',current.reshape(1,-1))
# d,i = nbrs.kneighbors(current.reshape(1,-1))
# recs = i[0]
# # print('\nd: \n',d)
# # print('\ni: \n',i)

# full_recs = []
# for i in range(0,5):
#     x = recs[i]
#     # print('x: ',x)
#     # full_recs[i] = fonts.loc[fonts['idx'] == x]
#     full_recs.append(fonts.iloc[x])

# print('\nrecommendations:\n',full_recs)


# ************* Test K Value and Distance Metric *************
# k val must be > 5
font = 'Open Sans 400'
num_neighbors = 5

def test_k_val_distance(k,metric,font,fonts,vectors,num_neighbors):
    filename = 'recs_k' + str(k) + '_' + metric + '.csv'
    distance = ''
    print(metric)

    if k <= 5:
        print("K must be greater than 5")
    elif metric == 'c':
        distance = 'cosine'
    elif metric == 'e':
        distance = 'euclidean'
    else:
        print("Invalid metric")

    knn = NearestNeighbors(n_neighbors=k, metric=distance, algorithm='auto').fit(vectors)
    recs= get_font_combinations(font,fonts,vectors,knn,num_neighbors)

    # for i in range(0,len(recs)):
    #     webbrowser.open_new(recs[i]['url'])

    df = pd.DataFrame(recs)
    df.to_csv(filename, index=None, header=True)

    return df


# recsk6c = test_k_val_distance(6,'c',font,fonts,font_vectors,num_neighbors)
# webbrowser.open_new('www.google.com')
# recsk6e = test_k_val_distance(6,'e',font,fonts,font_vectors,num_neighbors) # like this one better

# recsk100c = test_k_val_distance(100,'c',font,fonts,font_vectors,num_neighbors)
# webbrowser.open_new('www.google.com')
# recsk100e = test_k_val_distance(100,'e',font,fonts,font_vectors,num_neighbors)

# recsk200c = test_k_val_distance(200,'c',font,fonts,font_vectors,num_neighbors)
# webbrowser.open_new('www.google.com')
# recsk200e = test_k_val_distance(200,'e',font,fonts,font_vectors,num_neighbors)

# knn_k4_c = NearestNeighbors(n_neighbors=4, metric='cosine', algorithm='auto').fit(font_vectors)
# recs_k4_c = get_font_combinations(font,fonts,font_vectors,knn_k4_c,num_neighbors)
# df_k4c = pd.DataFrame(knn_k4_c)
# df_k4c.to_csv(r'k4c.csv', index=None, header=True)


# knn_k4_e = NearestNeighbors(n_neighbors=4, metric='euclidean', algorithm='auto').fit(font_vectors)
# recs_k4_e = get_font_combinations(font,fonts,font_vectors,knn_k4_e,num_neighbors)
# df_k4e = pd.DataFrame(knn_k3_e)
# df_k4e.to_csv(r'k4e.csv', index=None, header=True)



# ************* Test Distance Metric *************