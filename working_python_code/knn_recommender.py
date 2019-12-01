import os, webbrowser
import pandas as pd
from scipy.spatial import distance
from sklearn.neighbors import NearestNeighbors
from preprocess_data_gf import *
# from helper_functions import *
# from similarity import *
# from knn_scratch import *

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

def get_font_combinations(font,fonts,vectors,knn,num_recs):
    # Get font object and find corresponding vector
    font_obj = fonts.loc[font]
    idx = font_obj['idx']
    choice = vectors[idx]

    # Get k nearest vectors for specified font
    # distances,indices = knn.kneighbors(choice.reshape(1,-1))
    distances,indices = knn.kneighbors([choice])
    # print(distances)
    # print('knn indices: ',indices)
    sim_vectors = indices[0]
    diff_vectors = np.flipud(sim_vectors)
    print('sim_vectors: ',sim_vectors)
    print('diff_vectors',diff_vectors)

    # Use recommended vectors to find corresponding font objects
    similar = []
    dissimilar = []
    full_recs = []
    for i in range(0,num_recs):
        curr_rec = sim_vectors[i]
        full_recs.append(fonts.iloc[curr_rec])

        curr_sim = sim_vectors[i]
        curr_dis = diff_vectors[i]
        similar.append(fonts.iloc[curr_sim])
        dissimilar.append(fonts.iloc[curr_dis])

    full_recs.append(similar)
    full_recs.append(dissimilar)

    return full_recs, similar, dissimilar

    # Instead of using built in function, pass in indices from original knn object and create two copies: the original and the reversed. Then calculate distances using those to find nearest/furthest neighbors

    # Create dictionary of font object:vector
    font_dict = {}
    indices = fonts['idx'].tolist()

    for i in range(0,len(vectors)):
        index = indices[i]
        font_dict[index] = vectors[i]

    # Calculate euclidean distance between chosen font and all other fonts
    distances = []
    font_vec = vectors[idx]
    for entry in font_dict:
        curr_vec = font_dict[entry]
        dist = distance.euclidean(font_vec,curr_vec)
        distances.append([entry,dist])

    # Get most similar (smallest) distances and most dissimilar (farthest) distances
    similar = sorted(distances)
    dissimilar = sorted(distances, reverse=True)
    # print('similar: ',similar)
    # print('dissimilar: ',dissimilar)

    # # Use recommended vectors to find corresponding font objects
    sim = []
    dis = []
    full_recs = []
    for i in range(0,num_recs):
        curr_sim = similar[i]
        curr_dis = dissimilar[i]
        sim.append(fonts.iloc[curr_sim])
        dis.append(fonts.iloc[curr_dis])

    full_recs.append(sim)
    full_recs.append(dis)
    # return full_recs,similar[1:k+1],dissimilar[0:k] # Return k most similar fonts (excluding self) and k most dissimilar fonts
    return full_recs, sim, dis

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

print('\n******* sklearn version *******\n')
nbrs = NearestNeighbors(n_neighbors=len(ohe_vectors), metric='euclidean', algorithm='auto').fit(ohe_vectors)
distances, indices = nbrs.kneighbors(ohe_vectors)
print(indices[0][1:])
print('distances:\n',distances)
print('indices:\n',indices)
full_recs,sim,dis = get_font_combinations(font_name,fonts,ohe_vectors,nbrs,5)
print(full_recs)
print('sim:\n',sim)
print('\ndis:\n',dis)