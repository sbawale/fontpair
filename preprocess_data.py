import json, urllib.request, re
import pandas as pd
from contextlib import closing

# font weights:
# thin = 100
# extra light = 200
# light = 300
# regular = 400
# medium = 500
# semibold = 600
# bold = 700
# extra bold = 800
# black = 900

# Initialize font lists for both databases
gf = []
fs = []

# Import Google Fonts metadata
with closing(urllib.request.urlopen("https://www.googleapis.com/webfonts/v1/webfonts?sort=alpha&key=AIzaSyAMBY2XP1dQ67L3SX2rOOrZ505Is99Fm40")) as urlGF:
    gfData = json.loads(urlGF.read().decode())
    fontlist = gfData['items'] # Get actual list of fonts (Google wraps them in a 2-column list for some reason)

    for font in fontlist:
        # Initialize feature variables
        name = ""
        family = font['family']
        category = font['category']
        italic = 0 # default is 0: not italic
        weight = 400 # default is regular
        variants = font['variants']

        # Create tuple to be appended to list
        current = {}
        current['name'] = name
        current['family'] = family
        current['category'] = category
        current['italic'] = italic
        current['weight'] = weight

        # Check for font variants
        if len(variants) > 1:
            for var in variants:
                # Get weight
                temp = var.split("00")
                if len(temp) == 1:
                    weight = 400
                else:
                    weight = int(temp[0])*100

                # Get name based on weight
                if weight == 100:
                    name = family + " Thin"
                elif weight == 200:
                    name = family + " ExtraLight"
                elif weight == 300:
                    name = family + " Light"
                elif weight == 500:
                    name = family + " Medium"
                elif weight == 600:
                    name = family + " SemiBold"
                elif weight == 700:
                    name = family + " Bold"
                elif weight == 800:
                    name = family + " ExtraBold"
                elif weight == 900:
                    name = family + " Black"
                else:
                    name = family + " Regular"

                # Check if italic
                if len(temp) > 1 and temp[1] == 'italic':
                    italic = 1
                    name = name + " Italic"

                # Append to gf list
                print(name)
                gf.append(current)

#print(gf)
# Import Fontsquirrel metadata
with closing(urllib.request.urlopen("http://www.fontsquirrel.com/api/fontlist/all")) as urlFS:
    fsData = json.loads(urlFS.read().decode())

    for font in fsData:
        # Initialize feature variables
        name = ""
        family = font['family_name']
        category = font['classification']
        italic = 0 # default is 0: not italic
        weight = 400 # default is regular
        numVariants = int(font['family_count'])

        # Create tuple to be appended to list
        current = {}
        current['name'] = name
        current['family'] = family
        current['category'] = category
        current['italic'] = italic
        current['weight'] = weight

        # Clean up category features
        c = category.lower()
        # if c == 'dingbat': # exclude dingbat
        #     continue
        if c == 'monospaced':
            category = 'monospace'
        elif c == 'handdrawn':
            category = 'handwriting'
        else:
            category = c

        # Check for font variants
        if numVariants > 1:
            # Get information about the current font's variants
            variantURL = "https://www.fontsquirrel.com/api/familyinfo/" + font['family_urlname']
            with closing(urllib.request.urlopen(variantURL)) as v:
                varData = json.loads(v.read().decode())

            for var in varData:
                # f = var['family_name'] + " " + var['style_name']
                # current['name'] = f

                # Get variant name

                # # Split font style into words based on capital letters
                # styleWords = re.findall('[A-Z][^A-Z]*', font['style_name'])

                # # Change style phrasings to match GF phrasings

                # # Add a space after all but the last word
                # for i in range(0,len(styleWords)-1):
                #     styleWords[i] = styleWords[i] + " "

                # # Combine style with family to create variant name
                # name = (family + " ").join(styleWords)
                family = var['family_name']
                name = family + " " + var['style_name']
                #print("var: ",var)
                # Get weight based on name
                if 'ExtraLight' in name:
                    weight = 200
                elif 'SemiBold' in name:
                    weight = 600
                elif 'ExtraBold' in name:
                    weight = 800
                elif 'Thin' in name:
                    weight = 100
                elif 'Light' in name:
                    weight = 300
                elif 'Medium' in name:
                    weight = 500
                elif 'Bold' in name:
                    weight = 700
                elif 'Black' in name:
                    weight = 900
                else:
                    weight = 400

                # Check if italic
                if 'italic' in name:
                    italic = 1

                # Append to list
                print("name: ",name)
                fs.append(current)

# Convert lists to dataframes
col_names =  ['name', 'family', 'category','italic','weight']
dfGF = pd.DataFrame(gf, columns = col_names)
dfFS = pd.DataFrame(fs, columns = col_names)
print(dfGF)
print(dfFS)

# Merge dataframes into one, getting rid of duplicates at the same time
dataset = dfGF.merge(dfFS, left_on='name', right_on='name')
print(dataset)