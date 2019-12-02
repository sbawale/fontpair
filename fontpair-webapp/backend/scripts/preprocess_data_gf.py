import json, urllib.request, re, csv, os
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
    # filepath = 'data/' + filename
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

def preprocess_data_gf():
    # Initialize font list, column/feature names, array of font weights, and get ambiguous families
    google_fonts = []
    [families,serifs] = get_unlabeled_families('data/label_by_hand.csv')
    col_names =  ['name','family','category','is_body','is_serif','is_italic','weight','url']
    font_weights = ['thin','extralight','light','regular','medium','semibold','bold','extrabold','black']
    font_weights_num = [100, 200, 300, 400, 500, 600, 700, 800, 900]

    # *************** IMPORT AND RESTRUCTURE GOOGLE FONTS DATA ***************

    with open('data/data_google_fonts.json') as json_file:
        data = json.load(json_file)
        fontlist = data['items'] # Get actual list of fonts (Google wraps them in a 2-column list for some reason)
        print('Loading Google Fonts data...\n')
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
            weight = 'regular' # default is 400: regular
            url = 'http://fonts.google.com/specimen/' + font['family'].replace(' ','+')

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
                    var_weight = var.split("00")
                    if len(var_weight) == 1:
                        weight = 400
                    else:
                        weight = int(var_weight[0])*100

                    # Get name based on weight
                    weight_idx = int((weight/100)-1)
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
                    current['url'] = url

                    # Print to console and append to google_fonts list
                    # print(name)
                    google_fonts.append(current)
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
                current['url'] = url

                # Print to console and append to google_fonts list
                # print(name)
                google_fonts.append(current)

    # *************** STANDARDIZE AND RETURN DATA ***************

    # Convert gf list to dataframe and add index column
    google_fonts_df = pd.DataFrame(google_fonts,columns=col_names)
    google_fonts_df['idx'] = google_fonts_df.index.tolist()
    google_fonts_df.to_csv(r'cleanedGF.csv', index=None, header=True)
    google_fonts_df.set_index('name',drop=True, append=False,inplace=True)

    print('Google Fonts data successfully processed!\n')
    return google_fonts_df