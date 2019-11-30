import csv, webbrowser
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder

def split_train_test_val(data, train_ratio):
    data_copy = data.copy()
    train_set = data_copy.sample(frac=train_ratio, random_state=0)
    test_set = data_copy.drop(train_set.index)

    train_copy = train_set.copy()
    train_set = train_copy.sample(frac=train_ratio,random_state=0)
    val_set = train_copy.drop(train_set.index)

    return train_set, test_set, val_set


def check_if_serif(family,category):
    if category == 'serif' or 'serif' in family:
        return 1
    elif category == 'sans-serif' or 'sans' in family:
        return 0
    elif category == 'handwriting':
        return 0 # handwriting fonts are classified as sans-serif
    elif category == 'monospace':
        return 1 # monospaced fonts are classified as serif
    else:
        return -1 # mark as ambiguous so can label by hand later

def get_unlabeled_families(filename):
    families = []
    serifs = []

    # Read in CSV file of hand labeled font families (serif/sans-serif)
    with open(filename) as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader) # skip header/first line
        for row in csvreader:
            family = row[0]
            serif = row[1]
            families.append(family)
            serifs.append(serif)

    return families, serifs

def get_unique_strings(dataset,feature_index):
    unique = []
    for font in dataset.itertuples(index=False,name=None):
        # Split current value into individual words based on whitespace
        feature = font[feature_index].split()
        for word in feature:
            if word not in unique:
                unique.append(word)
    return unique

def get_font_vectors_tfidf(fonts, include_family):
    # Convert all features (weight, category, etc.) to single bag of words
    bags_of_words = []

    for font in fonts.itertuples(index=False,name=None):
        if include_family:
            family = font[1].split()
            no_digits = "".join(filter(lambda x: not x.isdigit(), family))
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
    print('\nattempting to create vectors...\n')
    tfidf = TfidfVectorizer(ngram_range=(1, 1), min_df=0.0001)
    tfidf_matrix = tfidf.fit_transform(bags_of_words)
    vectors = tfidf_matrix
    print('successfully vectorized fonts!')

    # Create new dataframe with 4 columns: font name, original bag of words, vector, id
    print("\ncreating new dataframe...\n")
    # print(fonts.head())
    # print(fonts.index.tolist())
    font_dict = {}
    font_dict['name'] = fonts.index.tolist()
    font_dict['bag_of_words'] = bags_of_words
    font_dict['vector'] = vectors

    font_dict = pd.DataFrame(font_dict)
    font_dict['id'] = font_dict.index.tolist()
    # font_dict = pd.DataFrame(fonts.index.tolist(), columns=['name','bags_of_words','vectors','id'])
    # font_dict = fonts.index.tolist() #fonts['name']
    # font_dict.insert(1, bags_of_words)
    # font_dict.insert(2, vectors)
    # font_dict.insert(3, font_dict.index.tolist())
    font_dict.set_index(font_dict['name'], drop=True, append=False, inplace=True, verify_integrity=False)
    # font_dict.to_csv('vectortest.csv')
    print("\ndataframe created!\n")

    return vectors, font_dict

def get_font_combinations(font,fonts,vectors,knn,num_recs):
    # Get font object and find corresponding vector
    font_obj = fonts.loc[font]
    idx = font_obj['idx']
    # choice = vectors[idx]
    choice = vectors.loc[font]
    # print(idx)

    # Get k nearest vectors for specified font
    # distances,indices = knn.kneighbors(choice.reshape(1,-1))
    distances,indices = knn.kneighbors([choice])
    # print(distances)
    rec_vectors = indices[0]

    # Use recommended vectors to find corresponding font objects
    full_recs = []
    for i in range(0,num_recs):
        curr_rec = rec_vectors[i]
        full_recs.append(fonts.iloc[curr_rec])
        # webbrowser.open_new(full_recs[i]['url'])

    return full_recs

# def one_hot_encode_font(font):
#     ohe_font = pd.concat(
#         [font["category"].str.get_dummies(sep=","),
#         pd.get_dummies(font[["weight"]]),
#         font[["is_body"]],
#         font[["is_serif"]],
#         font["is_italic"]],
#         axis=1)
#     return ohe_font

# def get_font_vectors_ohe(fonts):
#     ohe_fonts = pd.concat(
#         # [fonts["category"].str.get_dummies(sep=","),
#         [pd.get_dummies(fonts[['category']]),
#         pd.get_dummies(fonts[['weight']]),
#         fonts[['is_body']],
#         fonts[['is_serif']],
#         fonts['is_italic']],
#         axis=1)
#     min_max_scaler = MinMaxScaler()
#     font_vectors = min_max_scaler.fit_transform(ohe_fonts)
#     return font_vectors