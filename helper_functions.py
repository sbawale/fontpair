import json, urllib.request, re, csv
import pandas as pd
import numpy as np
from contextlib import closing

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
        # Split current value into individual words
        feature = font[feature_index].split()
        for word in feature:
            if word not in unique:
                unique.append(word)
    return unique

def vectorize_font(font,names,families,features):
    # colNames =  ['name','family','category','is_body','is_serif','is_italic','weight']
    # features = ['body','display','handwriting','monospace','serif','sans-serif','italic','weight']

    # Instantiate sub vectors
    name_vector = [0]*len(names)
    family_vector = [0]*len(families)
    feature_vector = [0]*len(features)

    # Convert name and family to list of individual words
    name = font[0].split()
    family = font[1].split()

    # Convert name and family to vector
    for i in range(0,len(names)):
        if names[i] in name:
            name_vector[i] = 1

    for i in range(0,len(families)):
        if families[i] in family:
            family_vector[i] = 1

    # Get the remaining features, check values for each feature
    feature_vector[0] = font[3] # body
    feature_vector[1] = int(font[2] == 'display') # category
    feature_vector[2] = int(font[2] == 'handwriting') # category
    feature_vector[3] = int(font[2] == 'monospace') # category
    feature_vector[4] = font[4] # serif
    feature_vector[5] = int(not font[4]) # sans-serif
    feature_vector[6] = font[5] # italic
    feature_vector[7] = font[6]/1000 # weight
    # need to scale weight somehow... maybe divide by 1000? or do another bag of words?

    # Combine sub vectors into complete font vector
    font_vector = name_vector + family_vector + feature_vector
    return font_vector