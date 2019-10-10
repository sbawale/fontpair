import json, urllib.request, re
import pandas as pd
from contextlib import closing

def get_googlefonts_data(fontWeights,colNames):
    # Initialize font list for Google Fonts database
    googleFonts = []

    # Import data
    with closing(urllib.request.urlopen("https://www.googleapis.com/webfonts/v1/webfonts?sort=alpha&key=AIzaSyAMBY2XP1dQ67L3SX2rOOrZ505Is99Fm40")) as url:
        data = json.loads(url.read().decode())
        fontlist = data['items'] # Get actual list of fonts (Google wraps them in a 2-column list for some reason)
        print("Loading Google Fonts data...")
        for font in fontlist:
            print("********************************************")
            # Initialize feature variables
            name = ""
            family = font['family'].strip()
            category = font['category'].strip()
            italic = 0 # default is 0: not italic
            weight = 400 # default is 400: regular

            # Create tuple to be appended to list
            current = {}
            print(family)
            # Check for font variants
            variants = font['variants']
            print("variants: ",variants)
            if len(variants) > 1:
                for var in variants:
                    # Get weight
                    temp = var.split("00")
                    #print("temp: ",temp)
                    if len(temp) == 1:
                        weight = 400
                    else:
                        weight = int(temp[0])*100

                    # Get name based on weight
                    weightIndex = int((weight/100)-1)
                    name = family + " " + fontWeights[weightIndex]

                    # Check if italic
                    #if len(temp) > 1 and temp[1] == 'italic':
                    if 'italic' in temp:
                        italic = 1
                        name = name + " Italic"

                    # Assign values to current tuple
                    current['name'] = name
                    current['family'] = family
                    current['category'] = category
                    current['italic'] = italic
                    current['weight'] = weight

                    # Print to console and append to gf list
                    print(current,"\n")
                    # print(name)
                    googleFonts.append(current)
                    tempdf = pd.DataFrame(googleFonts)
                    print(tempdf.tail())
            else:
                name = family

                # Assign values to current tuple
                current['name'] = name
                current['family'] = family
                current['category'] = category
                current['italic'] = italic
                current['weight'] = weight

                # Print to console and append to gf list
                print(current,"\n")
                # print(name)
                googleFonts.append(current)

    # Convert list to dataframe and return dataframe
    googleFontsDF = pd.DataFrame(googleFonts, columns = colNames)
    # googleFontsDF.drop_duplicates(keep='first').reset_index(drop=True)
    return googleFontsDF