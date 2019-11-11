import json, urllib.request, re
import pandas as pd
from contextlib import closing
from helper_functions import *

def preprocess_data():
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

    # *************** IMPORT AND CLEAN FONTSQUIRREL DATA ***************

    # with closing(urllib.request.urlopen("http://www.fontsquirrel.com/api/fontlist/all")) as urlFS:
    #     fsData = json.loads(urlFS.read().decode())
    # with open('fontsquirrel-fonts.json') as json_file:
    #     fsData = json.load(json_file)
    #     print("Loading FontSquirrel data...")
    #     for font in fsData:
    #         # Initialize feature variables
    #         name = ""
    #         family = font['family_name'].strip()
    #         category = font['classification'].strip().lower()
    #         italic = 0 # default is 0: not italic
    #         weight = 400 # default is regular

    #         # Clean up family name
    #         #print("family 1: ",family)
    #         # familyWords = re.findall('[A-Z][^A-Z]*', family)
    #         # if len(familyWords) > 1:
    #         #     family = familyWords[0]
    #         #     for i in range(0,len(familyWords)):
    #         #         family = " " + family + familyWords[i]
    #         #print("family 2: ",family)
    #         # Clean up category features
    #         # if category == 'dingbat':
    #         #     # Exclude dingbat
    #         #     continue
    #         if category == 'monospaced':
    #             category = 'monospace'
    #         elif category == 'handdrawn':
    #             category = 'handwriting'
    #         elif category == 'sans serif':
    #             category = 'sans-serif'
    #         else:
    #             category = category

    #         # Check for font variants
    #         numVariants = int(font['family_count'])
    #         if numVariants > 1:
    #             # Get information about the current font's variants
    #             variantURL = "https://www.fontsquirrel.com/api/familyinfo/" + font['family_urlname']
    #             with closing(urllib.request.urlopen(variantURL)) as v:
    #                 varData = json.loads(v.read().decode())

    #             for var in varData:
    #                 # Get variant name
    #                 #print("has variants")
    #                 #print(var)
    #                 # Split font style into words based on capital letters
    #                 #print("style 1: ",var['style_name'].strip())
    #                 # varStyle = var['style_name'].strip()
    #                 # styleWords = re.findall('[A-Z][^A-Z]*', var['style_name'].strip())
    #                 # varStyle = styleWords[0]
    #                 # print(styleWords)
    #                 # # print(var['style_name'].strip() in family)
    #                 # if len(styleWords) > 1:
    #                 #     # Change style phrasings to match GF phrasings and
    #                 #     # add space after all but last word
    #                 #     for i in range(0,len(styleWords)-1):
    #                 #         varStyle = " " + varStyle + styleWords[i].strip()

    #                 # if (varStyle in family) and (varStyle in fontWeights):
    #                 #     style = ""
    #                 # else:
    #                 #     style = varStyle
    #                 # #print("style 2: ",style)
    #                 # # # Combine style with family to create variant name
    #                 # varName = re.findall('[A-Z][^A-Z]*', var['fontface_name'].strip())
    #                 # print(varName)
    #                 # #print(varName)
    #                 # style = varName[0]
    #                 # if len(varName) > 1:
    #                 #     for i in range(1,len(varName)):
    #                 #         style = style + " " + varName[i]


    #                 # family = var['family_name'].strip()
    #                 name = var['family_name'] + " " + var['style_name'].strip()
    #                 # name = style
    #                 #print(name)
    #                 #print("var: ",var)
    #                 # Get weight based on name
    #                 for i in range(0,len(fontWeights)):
    #                     if fontWeights[i] in name:
    #                         weight = i*100
    #                         break

    #                 # Check if italic
    #                 if 'Italic' in name:
    #                     italic = 1

    #                 # Create tuple to be appended to list
    #                 #current = {}
    #                 current['name'] = name
    #                 current['family'] = family
    #                 current['category'] = category
    #                 current['italic'] = italic
    #                 current['weight'] = weight

    #                 # Print to console and append to fs list
    #                 print(current)
    #                 # print(name)
    #                 fs.append(current)
    #         else:
    #             name = family
    #             #print(name)

    #             # Create tuple to be appended to list
    #             #current = {}
    #             current['name'] = name
    #             current['family'] = family
    #             current['category'] = category
    #             current['italic'] = italic
    #             current['weight'] = weight

    #             # Print to console and append to fs list
    #             print(current)
    #             # print(name)
    #             fs.append(current)

    # dfFS = pd.DataFrame(fs, columns = col_names)
    # print("FontSquirrel data successfully loaded.\n")

    # *************** COMBINE DATAFRAMES ***************


    # print("Google Fonts dataframe:\n",dfGF.head(n=20))
    # print("FontSquirrel dataframe:\n",dfFS.head(n=20))

    # Combine dataframes into one, getting rid of duplicates at the same time
    # dataset = pd.merge(dfGF,dfFS,on='name')
    # dataset = pd.concat([dfGF,dfFS]).drop_duplicates(keep='first').reset_index(drop=True)
    # print("Dataset:\n",dataset.head(n=20))
    # return dataset

test = preprocess_data()
# label_me = []

# # Get all fonts with is_serif = -1 from test
# for font in test:
#     if font['is_serif'] == -1:
#         label_me.append(font)

# print(label_me)