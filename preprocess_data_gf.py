import json, urllib.request, re
import pandas as pd
from contextlib import closing
from helper_functions import *

def preprocess_data_gf():
    # Initialize font list, column/feature names, array of font weights, and get ambiguous families
    gf = []
    label_me = []
    col_names =  ['name','family','category','is_body','is_serif','is_italic','weight']
    fontWeights = ['Thin','Extra Light','Light','Regular','Medium',
                   'Semi Bold','Bold','Extra Bold','Black']
    [families,serifs] = get_unlabeled_families('label_by_hand.csv')
    # Corresponding numerical weights: [100, 200, 300, 400, 500, 600, 700, 800, 900]

    # *************** IMPORT AND CLEAN GOOGLE FONTS DATA ***************

    with open('google-fonts.json') as json_file:
        gfData = json.load(json_file)
        fontlist = gfData['items'] # Get actual list of fonts (Google wraps them in a 2-column list for some reason)
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

    # Convert gf list to dataframe
    dfGF = pd.DataFrame(gf, columns = col_names)
    print("\nGoogle Fonts data successfully loaded!\n")
    return dfGF

# ***************** TESTING *****************

# test = preprocess_data_gf()
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(test)
# test.to_csv(r"testgf.csv", index = None, header=True)

# test2 = get_unlabeled_families(test)
# print(test2)