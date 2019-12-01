import csv, os
from fonts.models import *
from families.models import *
from categories.models import *

# Import data from individual CSV files

def run():
    # Import fonts
    with open('data/cleanedGF.csv') as csvfile_fonts:
        reader = csv.DictReader(csvfile_fonts)
        for row in reader:
            f = Font(name=row['name'],
                 family=row['family'],
                 category=row['category'],
                 is_body=row['is_body'],
                 is_serif=row['is_serif'],
                 is_italic=row['is_italic'],
                 weight=row['weight'],
                 url=row['url'])
            f.save()

    # Import families
    with open('data/families.csv',mode='r',encoding='utf-8-sig') as csvfile_families:
        reader = csv.DictReader(csvfile_families)
        for row in reader:
            fm = Family(name=row['name'])
            fm.save()

    # Import categories
    with open('data/categories.csv',mode='r',encoding='utf-8-sig') as csvfile_categories:
        reader = csv.DictReader(csvfile_categories)
        for row in reader:
            c = Category(name=row['name'])
            c.save()

    # Import weights
    with open('data/test-weight.csv',mode='r',encoding='utf-8-sig') as csvfile_weights:
        reader = csv.DictReader(csvfile_weights)
        for row in reader:
            w = Weight(weight=row['weight'], string=row['string'])
            w.save()