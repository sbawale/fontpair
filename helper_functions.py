import json, urllib.request, re
import pandas as pd
import numpy as np
from contextlib import closing
from itertools import chain
from collections import Counter, OrderedDict

# def check_if_serif(font,family):
#     category_font = font['category']
#     category_family = family['category']

#     if category_font == 'serif' or category_family == 'serif':
#         return 1
#     elif category_font == 'sans-serif' or category_family == 'sans-serif':
#         return 0
#     elif category_font == 'handwriting' or category_family == 'handwriting':
#         return 0 # handwriting fonts are classified as sans-serif
#     elif category_font == 'monospace' or category_family == 'monospace':
#         return 1 # monospaced fonts are classified as serif
#     else:
#         return -1 # mark as ambiguous so can label by hand later

# def check_if_serif(*font):
#     category = font[2]

def check_if_serif(family,category):
    # category_font = font['category']

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
        # look up family in hand-labeled dataset?

def label_serif(fonts,file):
    # fonts is the label_me list
    # file is file with name-serif mapping
    for f in fonts:
        print(f['family'])
        f['is_serif'] = input('is_serif: ')

def get_unique_strings(database,tuple_attribute):
    unique = []
    for font in database:
        if font[tuple_attribute] not in unique:
            unique.append(font[tuple_attribute])
    # unique.sort()
    return unique

def vectorize_font(font,names,categories):
    name_vector = zeros(len(names))
    category_vector = zeros(len(categories))
    serif_vector = zeros(1)
    weight_vector = font['weight'] # need to scale somehow... maybe divide by 1000?

    # HAAAALP
    # ahem I mean iterate through arrays and find matches; mark as 1
    for i in range(0,len(names)):
        if names[i] in font['name']:
            name_vector[i] = 1

    for i in range(0,len(categories)):
        # Check values for each feature
        print("help")

    # Combine individual vectors into final font vector
    font_vector = name_vector + feature_vector + serif_vector + weight_vector
    return font_vector

def get_font_vectors(fonts,names,features):
    vectors = []
    for f in fonts:
        current = vectorize_font(f,names,features)
        vectors.append(current)
    return vectors