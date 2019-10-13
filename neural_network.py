import json, urllib.request
import pandas as pd
import numpy as np
from contextlib import closing
from itertools import chain
from collections import Counter, OrderedDict

# Font categories: serif, sans-serif, display, handwriting, monospace
# possibly add isbodyText as a category?

# Get helper methods
from preprocess_data import preprocess_data
from get_googlefonts_data import get_googlefonts_data
from helper_functions import *

# Get preprocessed data from Google Fonts API
fontWeights = ['Thin','Extra Light','Light','Regular','Medium',
                'Semi Bold','Bold','Extra Bold','Black']
# corresponding numerical weights: [100, 200, 300, 400, 500, 600, 700, 800, 900]
colNames =  ['name', 'family', 'category','italic','weight']

fonts = get_googlefonts_data(fontWeights,colNames)
print(fonts.tail(50))

# Load database

# create list of all unique words in font names
# create list of features
unique_names = get_unique_strings(fonts,'name')
is_serif = zeros(1)
features = ['body', 'display', 'handwriting', 'monospace']

# Need d-dimensional vector; at least 5???

# Learning task: find the x most similar fonts and the x most dissimilar fonts

# Assumptions:
# - "display" fonts do not pair well together
# - fonts from the same family pair well together
# - "handwriting" and "monospace" fonts do not pair well together
# -

# Map fonts to index and index to fonts
font_index = {fonts[0]: idx for idx, font in enumerate(fonts)}
book_index['Wire One']

# Do I create links from each font/index to every feature?