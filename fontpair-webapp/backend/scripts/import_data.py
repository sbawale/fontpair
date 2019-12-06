import csv, os
from fonts.models import *
from families.models import *
from categories.models import *
# from import_export import fields, resources
# from import_export.widgets import ForeignKeyWidget

# Import data from individual CSV files

def run():
    # Import categories
    with open('data/categories.csv',mode='r',encoding='utf-8-sig') as csvfile_categories:
        reader = csv.DictReader(csvfile_categories)
        for row in reader:
            c = Category(name=row['name'])
            c.save()

    # Import families
    with open('data/families.csv',mode='r',encoding='utf-8-sig') as csvfile_families:
        reader = csv.DictReader(csvfile_families)
        for row in reader:
            fm = Family(name=row['name'],
                        category=Category.objects.get(pk=row['category']),
                        url=row['url'])
            fm.save()

    # Import fonts
    with open('data/cleaned_data_gf.csv') as csvfile_fonts:
        # WEIGHTS = {
        #     'thin': 'Thin',
        #     'extralight': 'Extra Light',
        #     'light': 'Light',
        #     'regular': 'Regular',
        #     'medium': 'Medium',
        #     'semibold': 'Semi Bold',
        #     'bold': 'Bold',
        #     'extrabold': 'Extra Bold',
        #     'black': 'Black',
        # }

        reader = csv.DictReader(csvfile_fonts)
        for row in reader:
            f = Font(name=row['name'],
                # family=ForeignKeyWidget(Family, 'name'),
                family=Family.objects.get(pk=row['family']),
                # family=row['family'],
                # category=ForeignKeyWidget(Category, 'name'),
                category=Category.objects.get(pk=row['category']),
                # category=row['category'],
                is_body=row['is_body'],
                is_serif=row['is_serif'],
                is_italic=row['is_italic'],
                weight_num=row['weight_num'],
                weight_str=row['weight_str'])
            f.save()