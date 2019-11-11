import csv#, json, urllib.request, re,
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer#, TfidfTransformer, CountVectorizer
# from sklearn import preprocessing
# from sklearn.decomposition import PCA
# from sklearn_pandas import DataFrameMapper
# from sklearn.preprocessing import OneHotEncoder, LabelEncoder

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

def get_font_vectors(fonts, include_family):
    # Convert all features (weight, category, etc.) to single bag of words
    bags_of_words = []

    for font in fonts.itertuples(index=False,name=None):
        # try two types of recommenders: one with family included in the embeddings and one without the family in the embeddings
        if include_family:
            family = font[1].split()
            no_digits = "".join(filter(lambda x: not x.isdigit(), family))
            curr_bag = str(no_digits) + ' ' + font[2]
        else:
            curr_bag = font[2]

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
        curr_bag += body + serif + italic + ' ' + font[6]
        bags_of_words.append(curr_bag)

    # Convert bags of words to TF-IDF vectors
    # print(bags_of_words[0:5])
    print("\nattempting to create vectors...\n")
    tfidf = TfidfVectorizer(ngram_range=(1, 1), min_df=0.0001)
    tfidf_matrix = tfidf.fit_transform(bags_of_words)
    # print(tfidf_matrix[0:5])
    # print(tfidf_matrix.shape)
    # print(tfidf.get_feature_names())
    vectors = tfidf_matrix
    print("successfully vectorized fonts!")
    # print(vectors)
    # print(vectors.shape)

    print("\ncreating new dataframe...\n")
    # Create new dataframe with 3 columns: font name, original bag of words, vector
    font_dict = fonts[['name']];
    font_dict.insert(1, 'bag_of_words', bags_of_words)
    font_dict.insert(2, 'tfidf_vector', vectors)
    font_dict.to_csv('vectortest.csv')
    print(font_dict.head())
    print("\ndataframe created :)\n")
    return vectors, font_dict

    # instead of using a dictionary, create the data frame with font name (and possibly family) along with the embedding vector; search for the requested value in the embedding column then find the matching name/family

# def vectorize_font_names(fonts):
#     # Use count vectorizer instead???
#     # Initialize a CountVectorizer object: count_vectorizer
#     count_vec = CountVectorizer()

#     # Get bag of words for font names
#     # count_train = count_vec.fit(fonts['name'])
#     # unique_words = count_vec.transform(fonts['name'])
#     # # print(count_vec.get_feature_names())
#     # # print(words)
#     # print(fonts['name'])

#     # Create bag of unique words for names
#     unique_words = get_unique_strings(fonts,0)

#     # Can use count vectorizer OR get unique strings function

#     # Label encode names
#     labelencoder = LabelEncoder()
#     names = labelencoder.fit_transform(unique_words)
#     print(names)

#     # One-hot encode label-encoded names
#     onehotencoder = OneHotEncoder()
#     names = onehotencoder.fit_transform(names).toarray()

#     # Convert sparse one-hot encoded vectors to dense vectors

#     # This function must be called before splitting into train/test/val
#     # Concat vectorized names with feature embeddings?
#     return names

def vectorize_font(font,names,families,features,weights):
    # Use the "bag of words" encoding technique to turn fonts into vectors
    # colNames =  ['name','family','category','is_body','is_serif','is_italic','weight']
    # features = ['body','display','handwriting','monospace','serif','sans-serif','italic','weight']

    # Instantiate sub vectors
    name_vector = [0]*len(names)
    family_vector = [0]*len(families)
    feature_vector = [0]*len(features)
    weight_vector = [0]*len(weights)

    # Convert name and family to list of individual words
    name = font[0].split()
    family = font[1].split()

    # Convert name, family, and weight to respective vectors
    for i in range(0,len(names)):
        if names[i] in name:
            name_vector[i] = 1

    for i in range(0,len(families)):
        if families[i] in family:
            family_vector[i] = 1

    for i in range(0,len(weights)):
        if font[6] == weights[i]:
            weight_vector[i] = 1

    # Get the remaining features, check values for each feature
    feature_vector[0] = font[3] # body
    feature_vector[1] = int(font[2] == 'display') # category
    feature_vector[2] = int(font[2] == 'handwriting') # category
    feature_vector[3] = int(font[2] == 'monospace') # category
    feature_vector[4] = font[4] # serif
    feature_vector[5] = int(not font[4]) # sans-serif
    feature_vector[6] = font[5] # italic

    # Combine sub vectors into complete font vector
    font_vector = name_vector + family_vector + feature_vector + weight_vector
    # print("Vector size: ",len(font_vector)) # 2005 as of Oct 18
    return font_vector

def embed_font(font):
    # Reduce vector dimensionality using PCA

    # Convert font to dataframe
    embedded = pd.DataFrame(font)

    # Dimensionality reduction
    # Technique: PCA
    # Use embedding_column function instead???

    # Steps:
    # get data
    # explore data, understand original dimensionality
    # reshape to get new dimensionality?
    # convert to pd DataFrame
    # normalize data
    # standardize data
    #   StandardScaler -> fit_transform
    # reduce dimensionality
    #   PCA? --> most likely
    #   Gaussian Random Projection?
    #   MultiDimensional Scaling?
    #   Locally linear embedding?
    print("Leave me alone")