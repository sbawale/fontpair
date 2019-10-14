import json, urllib.request, re
import pandas as pd
from contextlib import closing
from helper_functions import *

def get_googlefonts_data():
    # Initialize font lists for both databases and array of font weights
    gf = []
    fs = []
    label_me = []
    col_names =  ['name','family','category','is_body','is_serif','italic','weight']
    fontWeights = ['Thin','Extra Light','Light','Regular','Medium',
                   'Semi Bold','Bold','Extra Bold','Black']
    # corresponding numerical weights: [100, 200, 300, 400, 500, 600, 700, 800, 900]

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
            is_body = category != 'display'
            is_serif = check_if_serif(family.lower(),category)
            italic = 0 # default is 0: not italic
            weight = 400 # default is 400: regular

            # Add families with is_serif = -1 to list of families to label by hand
            if is_serif == -1:
                # print(family)
                # is_serif = input(family + ' is_serif: ')
                label_me.append(family)

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

                    # Check if italic
                    if 'italic' in varWeight:
                        italic = 1
                        name = name + " Italic"

                    # Create tuple to be appended to list
                    current = {}
                    current['name'] = name
                    current['family'] = family
                    current['category'] = category
                    current['is_body'] = is_body
                    current['is_serif'] = is_serif
                    current['italic'] = italic
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
                current['italic'] = italic
                current['weight'] = weight

                # Print to console and append to gf list
                print(name)
                gf.append(current)

    # Convert gf list to dataframe
    dfGF = pd.DataFrame(gf, columns = col_names)
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     print(dfGF)
    # dfGF.to_csv(r"df.csv", index = None, header=True)
    print("\nGoogle Fonts data successfully loaded.\n")
    return dfGF

test = get_googlefonts_data()