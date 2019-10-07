import json, urllib.request, jsonmerge
from contextlib import closing
from jsonmerge import merge
from jsonmerge import Merger
from pprint import pprint

# Define font "node" class
class Font:
  def __init__(self, name, family, category):
    self.name = name
    self.family = family
    self.category = category
    # obliqueness - if not specified assume not oblique/italic
    # weight - if not specified assume normal

    # font weights:
    # thin = 100
    # light = 300
    # regular/medium = 400
    # bold = 700
    # black = 900

    # probably do this in the reading of json process, instead of having Font object
    def to_dict(self):
        return {'name': self.name,
                'family': self.family,
                'category': self.category}

# Initialize font lists for both databases
GoogleFonts = []
FontSquirrel = []

# Request URLS for databases
# "https://www.googleapis.com/webfonts/v1/webfonts?key=AIzaSyAMBY2XP1dQ67L3SX2rOOrZ505Is99Fm40"
# "http://www.fontsquirrel.com/api/fontlist/all"
# "https://www.fontsquirrel.com/api/familyinfo/{family}"

# Import Google Fonts metadata
with closing(urllib.request.urlopen("https://www.googleapis.com/webfonts/v1/webfonts?sort=alpha&key=AIzaSyAMBY2XP1dQ67L3SX2rOOrZ505Is99Fm40")) as urlGF:
    gfData = json.loads(urlGF.read().decode())
    items = gfData['items'] # Get actual list of fonts (Google wraps them in a 2-column list for some reason)

    for font in items:
        data = {}
        data['family'] = font['family']
        data['category'] = font['category']
        variants = font['variants']
        # print(family, font)

        # Check for font variants
        if len(variants) > 1:
            # Create a Font object for each variant and add to list
            for var in variants:
                f = font['family'] + " " + var.capitalize()
                data['id'] = f
                #print(data)
                json_dataGF = json.dumps(data)
        else:
            data['id'] = font['family']
            #print(data)
            json_dataGF = json.dumps(data)


    # For each font, select only the desired features
    # for font in items:
    #     family = font['family']
    #     category = font['category']
    #     variants = font['variants']
    #     # print(family, font)

    #     # Check for font variants
    #     if len(variants) > 1:
    #         # Create a Font object for each variant and add to list
    #         for var in variants:
    #             f = family + " " + var.capitalize()
    #             current = Font(f, family, category)
    #             GoogleFonts.append(current)
    #             # print(family, font)
    #             print(f)
    #     else:
    #         # Create new Font object and add to GoogleFonts list
    #         # print(family)
    #         current = Font(family, family, category)
    #         GoogleFonts.append(current)

# Import Fontsquirrel metadata
with closing(urllib.request.urlopen("http://www.fontsquirrel.com/api/fontlist/all")) as urlFS:
    fsData = json.loads(urlFS.read().decode())

    for font in fsData:
        data = {}
        data['family'] = font['family_name']
        #data['category'] = font['classification'].lower()
        numVariants = int(font['family_count'])
        # print(family, font)

        # Clean up category feature
        c = font['classification']

        if c == 'Dingbat':
            continue # exclude dingbat
        elif c == 'Blackletter' or c == 'Calligraphic':
            data['category'] = 'script'
        elif c == 'Comic' or c == 'Handdrawn':
            data['category'] = 'handwriting'
        elif c == 'Grunge' or c == 'Pixel':
            data['category'] = 'novelty'
        elif c == 'Programming':
            data['category'] = 'monospace'
        elif c == 'Retro' or c == 'Stencil':
            data['category'] = 'display'
        elif c == 'Slab-Serif' or c == 'Typewriter':
            data['category'] = 'serif'
        else:
            data['category'] = c.lower()

        # Check for font variants
        if numVariants > 1:
            # Get information about the current font's variants
            variantURL = "https://www.fontsquirrel.com/api/familyinfo/" + font['family_urlname']
            with closing(urllib.request.urlopen(variantURL)) as var:
                varData = json.loads(var.read().decode())
                #print(varData)
            for var in varData:
                #f = var['fontface_name']
                #print(var)
                f = var['family_name'] + " " + var['style_name']
                data['id'] = f
                #print(data)
                json_dataFS = json.dumps(data)
        else:
            data['id'] = font['family_name']
            #print(data)
            json_dataFS = json.dumps(data)

    # # For each font, select only the desired features
    # for font in fsData:
    #     family = font['family_name']
    #     category = font['classification'].lower()
    #     url = font['family_urlname']
    #     numVariants = font['family_count']
    #     print(family)

    #     # Check for font variants
    #     if int(numVariants) > 1:
    #         # Get information about the current font's variants
    #         variantURL = "https://www.fontsquirrel.com/api/familyinfo/" + url
    #         with closing(urllib.request.urlopen(variantURL)) as var:
    #             varData = json.loads(var.read().decode())

    #             # Create a Font object for each variant and add to list
    #             for var in varData:
    #                 f = var['fontface_name']
    #                 category = var['classification']
    #                 current = Font(f, family, category)
    #                 FontSquirrel.append(current)
    #                 #print(family)
    #     else:
    #         # Create new Font object and add to FontSquirrel list
    #         #print(family)
    #         current = Font(family, category)
    #         FontSquirrel.append(current)

schema = {
    "properties" : {
        "font": {
            #"type": "object",
            "mergeStrategy": "arrayMergeById",
            #"mergeOptions": {"idRef": "/family"}
        }
    }
}

merger = Merger(schema)
result = merger.merge(json_dataGF, json_dataFS)
pprint(result)
result_schema = merger.get_schema()
pprint(result_schema)

# FontSquirrel Format - want family_name, classification, family_count (will need to hunt down variations, this is just the number of variants)

# JSON FAMILIES LIST
# {
    # "id":"479",
    # "family_name":"1942 report",
    # "is_monocase":"N",
    # "family_urlname":"1942-report",
    # "foundry_name":"Johan Holmdahl",
    # "foundry_urlname":"Johan-Holmdahl",
    # "font_filename":"1942.ttf",
    # "classification":"Typewriter",
    # "family_count":"1"
# },

# JSON VARIANTS LIST
# {
    # "font_id":"2294",
    # "family_id":"1109",
    # "family_name":"Alegreya",
    # "style_name":"Regular",
    # "glyph_count":"503",
    # "filename":"Alegreya-Regular.otf",
    # "checksum":"2d1b252709aae7e71b23e33834d14ae5",
    # "is_monocase":"N",
    # "family_urlname":"alegreya",
    # "foundry_name":"Juan Pablo del Peral",
    # "foundry_urlname":"Juan-Pablo-del-Peral",
    # "classification":"Serif",
    # "family_count":"12",
    # "fontface_name":"AlegreyaRegular",
    # "listing_image":"https:\/\/imgs.fontbrain.com\/imgs\/2d\/1b\/252709aae7e71b23e33834d14ae5\/fsl-720-30-333333@2x.png","sample_image":"https:\/\/imgs.fontbrain.com\/imgs\/2d\/1b\/252709aae7e71b23e33834d14ae5\/sp-720x400-333333-penultimate@2x.png"
# },

# ------------------------------

# Google Fonts format - want family, category, variants
# {
#    "kind": "webfonts#webfont",
#    "family": "ABeeZee",
#    "category": "sans-serif",
#    "variants": [
#     "regular",
#     "italic"
#    ],
#    "subsets": [
#     "latin"
#    ],
#    "version": "v13",
#    "lastModified": "2019-07-17",
#    "files": {
#     "regular": "http://fonts.gstatic.com/s/abeezee/v13/esDR31xSG-6AGleN6tKukbcHCpE.ttf",
#     "italic": "http://fonts.gstatic.com/s/abeezee/v13/esDT31xSG-6AGleN2tCklZUCGpG-GQ.ttf"
#    }
#   },