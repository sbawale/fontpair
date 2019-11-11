import csv
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

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
