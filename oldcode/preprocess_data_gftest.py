import json, urllib.request, re
import pandas as pd
import numpy as np
import tensorflow as tf
from contextlib import closing
from sklearn import preprocessing
from helper_functions import *
from sklearn_pandas import DataFrameMapper

def preprocess_data_gf():
    # Initialize font list, column/feature names, array of font weights, and get ambiguous families
    gf = []
    [families,serifs] = get_unlabeled_families('label_by_hand.csv')
    col_names =  ['name','family','category','is_body','is_serif','is_italic','weight']
    fontWeights = ['Thin','Extra Light','Light','Regular','Medium',
                   'Semi Bold','Bold','Extra Bold','Black']
    # Corresponding numerical weights: [100, 200, 300, 400, 500, 600, 700, 800, 900]

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
            is_italic = 'roman' # default is 0/roman: not is_italic
            weight = 400 # default is 400: regular

            # Get serif status for fonts with is_serif = -1
            if is_serif == -1:
                for i, f in enumerate(families):
                    if f == family:
                        is_serif = serifs[i]

            # Check for font variants
            variants = font['variants']
            if len(variants) > 1:
                for var in variants:
                    # Get weight
                    varWeight = var.split("00")
                    if len(varWeight) == 1:
                        weight = 400
                    else:
                        weight = int(varWeight[0])*100

                    # Get name based on weight
                    weightIndex = int((weight/100)-1)
                    name = family + " " + fontWeights[weightIndex]
                    weight = fontWeights[weightIndex]

                    # Check if is_italic
                    if 'italic' in varWeight:
                        is_italic = 1
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
                    print(name)
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
                print(name)
                gf.append(current)

    # *************** STANDARDIZE AND RETURN DATA ***************

    # Convert gf list to dataframe
    dfGF = pd.DataFrame(gf,columns=col_names)
    # dfGF.to_csv(r"cleanedGF.csv", index = None, header=True)
    print(dfGF.head())
    return dfGF
    # Encode string features as labels for standardization
    le_name = preprocessing.LabelEncoder()
    le_family = preprocessing.LabelEncoder()
    le_category = preprocessing.LabelEncoder()

    dfGF['name'] = le_name.fit_transform(dfGF['name'])
    dfGF['family'] = le_family.fit_transform(dfGF['family'])
    dfGF['category'] = le_name.fit_transform(dfGF['category'])

    # Standardize data using Scaler
    scaler = preprocessing.StandardScaler()
    scaled_df = scaler.fit_transform(dfGF)
    scaled_df = pd.DataFrame(scaled_df, columns=col_names)
    # print(scaled_df.head())
    return scaled_df
    print(dfGF.head())

    # Reshape dataframe
    # cols = col_names.remove('name')
    # dfGF.pivot(index='name', columns='col_names', values=['family','category','is_body','is_serif','is_italic','weight'])
    # print(dfGF.head())

    # Standardize weight feature (continuous feature)
    # scaler = preprocessing.MinMaxScaler()
    # weight_df = pd.concat([dfGF['name'],dfGF['weight']],axis=1)
    # print(weight_df)
    # # weight_std = scaler.fit_transform(dfGF['weight'])
    # dfGF['weight'] = scaler.fit_transform(weight_df.transpose())
    # print(weight_df)



    # mapper = DataFrameMapper([(dfGF.columns, preprocessing.StandardScaler())])
    # scaled_features = mapper.fit_transform(dfGF.copy(), 4)
    # scaled_features_df = pd.DataFrame(scaled_features, index=dfGF.index, columns=dfGF.columns)



    scaler = MinMaxScaler()

    print("\nGoogle Fonts data successfully processed!\n")

# *************** HELPER FUNCTIONS ***************

def check_if_serif(family,category):
    if category == 'serif' or 'serif' in family:
        return 'serif'
    elif category == 'sans-serif' or 'sans' in family:
        return 'sans-serif'
    elif category == 'handwriting':
        return 'sans-serif' # handwriting fonts are classified as sans-serif
    elif category == 'monospace':
        return 'serif' # monospaced fonts are classified as serif
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

# ***************** DEBUGGING *****************

test = preprocess_data_gf()
# print(test)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(test)
# test.to_csv(r"testgf.csv", index = None, header=True)

# test2 = get_unlabeled_families(test)
# print(test2)