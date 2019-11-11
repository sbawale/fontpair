import json, urllib.request, re
import pandas as pd
import numpy as np
from contextlib import closing
from helper_functions import *

def filter_data_gf():
    # Initialize font list, column/feature names, array of font weights, and get ambiguous families
    gf = []
    [families,serifs] = get_unlabeled_families('label_by_hand.csv')
    col_names =  ['name','family','category','is_body','is_serif','is_italic','weight']
    # font_weights = ['Thin','Extra Light','Light','Regular','Medium',
    #                'Semi Bold','Bold','Extra Bold','Black']
    font_weights = ['thin','extralight','light','regular','medium','semibold','bold','extrabold','black']
    font_weights_num = [100, 200, 300, 400, 500, 600, 700, 800, 900]

    # *************** IMPORT AND RESTRUCTURE GOOGLE FONTS DATA ***************

    with open('data_google_fonts.json') as json_file:
        data = json.load(json_file)
        fontlist = data['items'] # Get actual list of fonts (Google wraps them in a 2-column list for some reason)
        print("Loading Google Fonts data...\n")
        for font in fontlist:
            # Check if font uses Latin alphabet, otherwise skip
            if 'latin' not in font['subsets']:
                continue
            elif 'Libre Barcode' in font['family']: # weird family that really should be dingbat
                continue

            # Initialize feature variables
            name = ""
            family = font['family'].strip()
            category = font['category'].strip()
            is_body = int(category != 'display')
            is_serif = check_if_serif(family.lower(),category)
            is_italic = 0 # default is 0: not is_italic
            # is_italic = 'roman'
            weight = 'regular' # default is 400: regular

            # Get serif status for fonts with is_serif = -1
            if is_serif == -1:
                for i, f in enumerate(families):
                    if f == family:
                        is_serif = serifs[i]

            # if is_serif:
            #     is_serif = 'serif'
            # else:
            #     is_serif = 'sans-serif'

            # if is_body:
            #     is_body = 'body'
            # else:
            #     is_body = 'heading'

            # Check for font variants
            variants = font['variants']
            if len(variants) > 1:
                for var in variants:
                    # Get weight
                    var_weight = var.split("00")
                    if len(var_weight) == 1:
                        weight = 400
                    else:
                        weight = int(var_weight[0])*100

                    # Get name based on weight
                    weight_idx = int((weight/100)-1)
                    # name = family + " " + font_weights[weight_idx]
                    name = family + " " + str(weight)
                    weight = font_weights[weight_idx]

                    # Check if is_italic
                    if 'italic' in var_weight:
                        is_italic = 1
                        # is_italic = 'italic'
                        name = name + " Italic"

                    # Create tuple to be appended to list
                    current = {}
                    current['name'] = name
                    current['family'] = family
                    current['category'] = category
                    current['is_body'] = is_body
                    current['is_serif'] = is_serif
                    current['is_italic'] = is_italic
                    current['weight'] = weight

                    # Print to console and append to gf list
                    # print(name)
                    gf.append(current)
            else:
                name = family

                # Create tuple to be appended to list
                current = {}
                current['name'] = name
                current['family'] = family
                current['category'] = category
                current['is_body'] = is_body
                current['is_serif'] = is_serif
                current['is_italic'] = is_italic
                current['weight'] = weight

                # Print to console and append to gf list
                # print(name)
                gf.append(current)

    # *************** STANDARDIZE AND RETURN DATA ***************

    # Convert gf list to dataframe
    dfGF = pd.DataFrame(gf,columns=col_names)
    dfGF.to_csv(r'cleanedGF.csv', index = None, header=True)
    # print(dfGF.head(10))
    print("\nGoogle Fonts data successfully processed!\n")
    return dfGF

# def get_bag_of_words(font,include_family):
#     # Convert all features (weight, category, etc.) to single bag of words
#     bags_of_words = []

#     if include_family:
#         family = font[1].split()
#         no_digits = "".join(filter(lambda x: not x.isdigit(), family))
#         curr_bag = str(no_digits) + ' ' + font[2]
#     else:
#         curr_bag = font[2]

#     # Get body value
#     if font[3] == 1: body = ' body'
#     else: body = ' heading'

#     # Get serif value
#     if font[4] == 1: serif = ' serif'
#     else: serif = ' sans-serif'

#     # Get italic value
#     if font[5] == 1: italic = ' italic'
#     else: italic = ' roman'

#     # Add the current bag to the list of all bags
#     curr_bag += body + serif + italic + ' ' + font[6]
#     bags_of_words.append(curr_bag)

def get_font_vectors(fonts, include_family):
    # Convert all features (weight, category, etc.) to single bag of words
    bags_of_words = []

    for font in fonts.itertuples(index=False,name=None):
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
    print("\nattempting to create vectors...\n")
    tfidf = TfidfVectorizer(ngram_range=(1, 1), min_df=0.0001)
    tfidf_matrix = tfidf.fit_transform(bags_of_words)
    vectors = tfidf_matrix
    print("successfully vectorized fonts!")

    # Create new dataframe with 3 columns: font name, original bag of words, vector
    print("\ncreating new dataframe...\n")
    font_dict = fonts[['name']]
    font_dict.insert(1, 'bag_of_words', bags_of_words)
    font_dict.insert(2, 'tfidf_vector', vectors)
    font_dict.insert(3, 'id', font_dict.index.tolist())
    font_dict.set_index('name', drop=True, append=False, inplace=True, verify_integrity=False)
    # font_dict.to_csv('vectortest.csv')
    print("\ndataframe created!\n")

    return vectors, font_dict