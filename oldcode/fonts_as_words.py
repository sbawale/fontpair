import json, urllib.request, re
import pandas as pd
import numpy as np
import tensorflow as tf
from contextlib import closing
from sklearn import preprocessing
from helper_functions import *
from sklearn_pandas import DataFrameMapper
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocess_data_gf import *

def get_font_embeddings(fonts):
    # Convert all features (weight, category, etc.) to single bag of words
    bags_of_words = []

    for font in fonts.itertuples(index=False,name=None):
        curr_bag = font[1] + ' ' + font[2]

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

    # Create new dataframe with the font name and the BOW as the only two columns
    to_vectorize = fonts[['name']];
    to_vectorize.insert(1, 'bag_of_words', bags_of_words)
    print(to_vectorize.head(10))

    # Convert vectors to embeddings
    tfidf = TfidfVectorizer(ngram_range=(1, 1), min_df=0.0001)
    tfidf_matrix = tfidf.fit_transform(to_vectorize['bag_of_words'])

    return tfidf_matrix

def embed_fonts(font_vectors):
    # fonts = preprocess_data_gf()
    # embeddings = get_font_embeddings(fonts)
    # print(embeddings[0:9])

    # instantiate CountVectorizer()
    cv=CountVectorizer()

    # generate word counts for words in fonts (excluding name)
    word_count_vector=cv.fit_transform(font_vectors['bag_of_words'])
    print(word_count_vector.shape)
    tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
    tfidf_transformer.fit(word_count_vector)

    # print idf values
    df_idf = pd.DataFrame(tfidf_transformer.idf_, index=cv.get_feature_names(),columns=["idf_weights"])

    # sort ascending
    df_idf.sort_values(by=['idf_weights'])
    # count matrix
    count_vector=cv.transform(font_vectors)

    # tf-idf scores
    tf_idf_vector=tfidf_transformer.transform(count_vector)


    feature_names = cv.get_feature_names()

    #get tfidf vector for first document
    first_document_vector=tf_idf_vector[0]

    #print the scores
    df = pd.DataFrame(first_document_vector.T.todense(), index=feature_names, columns=["tfidf"])
    df.sort_values(by=["tfidf"],ascending=False)

    # print(df_idf.head(10))
    print(df.head(10))

# TESTING AND DEBUGGING
fonts = preprocess_data_gf()
why = get_font_embeddings(fonts)
print(why)
# halp = embed_fonts(why)
# print(halp)