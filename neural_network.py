import json, urllib.request, re, csv
import pandas as pd
import numpy as np
from contextlib import closing

# Get helper methods
# from preprocess_data import preprocess_data
from preprocess_data_gf import preprocess_data_gf
from helper_functions import *

def build_neural_network():
    # Get preprocessed data from Google Fonts API
    colNames =  ['name','family','category','is_body','is_serif','is_italic','weight']
    fontWeights = ['Thin','Extra Light','Light','Regular','Medium',
                    'Semi Bold','Bold','Extra Bold','Black']
    # Corresponding numerical weights: [100, 200, 300, 400, 500, 600, 700, 800, 900]

    # Load font dataset
    fonts = preprocess_data_gf()

    # ***************** CONVERT FONT TUPLES TO VECTORS  *****************
    print("Converting font tuples to vectors...")

    # Create list of all unique words in font names and families
    names = get_unique_strings(fonts,0)
    families = get_unique_strings(fonts,1)

    # Create list of features (combination of category, is_body, is_serif, is_italic, and weight)
    features = ['body','display','handwriting','monospace','serif','sans-serif','italic','weight']

    # Convert all fonts to vectors and store in list
    vectors = []
    for f in fonts.itertuples(index=False,name=None):
        current = vectorize_font(f,names,families,features)
        vectors.append(current)

    print("All vectors created.")

    # ***************** CREATE EMBEDDINGS FROM VECTORS  *****************


def train_neural_network():
    print("No can do yet.")

def predict(neural_network,value):
    print("Definitely can't do yet.")

# ***************** TESTING *****************

test = build_neural_network()


# Need d-dimensional vector; at least 5???

# Learning task: find the x most similar fonts and the x most dissimilar fonts

# Assumptions:
# - "display" fonts do not pair well together
# - fonts from the same family pair well together
# - "handwriting" and "monospace" fonts do not pair well together