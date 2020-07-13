import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "laneige.settings")
django.setup()

from product.models import *

CSV_PATH_TOTAL = 'homme.csv'
#CSV_PATH_TOTAL = 'series.csv'

# def insert_category():
#     with open(CSV_PATH_TOTAL) as in_file:
#         data_reader = csv.reader(in_file)
#         next(data_reader, None)
#         for row in data_reader:
            
#             if row[0]:
#                 menu_name = row[0]
#                 menu_id = Menu.objects.get(name = menu_name).id
                
#             types = row[2]
#             types = types.split(',')

#             for type_name in types:
#                 type_name = type_name.strip(' ')
#                 type_name_id = Type.objects.get(name = type_name).id

#                 if not Category.objects.filter(
#                     menu_id = menu_id,
#                     type_name_id = type_name_id
#                     ).exists():
#                     print(menu_id, type_name_id)
#                     # Category.objects.create(
#                     #     menu_id = menu_id,
#                     #     type_name_id = type_name_id
#                     # )

def insert_product():
    with open(CSV_PATH_TOTAL) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:  

            name_ko = row[4]
            name_en = row[5]
            description = row[6]
            price = row[7]
            price = price.replace(',', '')
            price = int(price)
            volume = row[8]
            ingredient = row[11]
            feature = row[10]

            if not Product.objects.filter(
                name_ko = name_ko,
                name_en = name_en,
                description = description,
                price = price,
                volume = volume,
                ingredient = ingredient,
                feature = feature
                ).exists():
                Product.objects.create(
                    name_ko = name_ko,
                    name_en = name_en,
                    description = description,
                    price = price,
                    volume = volume,
                    ingredient = ingredient,
                    feature = feature
                )

def insert_product_categories():
    with open(CSV_PATH_TOTAL) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:

            product_name_ko = row[4]
            product_id = Product.objects.get(name_ko = product_name_ko).id

            if row[0]:
                menu_name = row[0]
                menu_id = Menu.objects.get(name = menu_name).id

            types = row[2]
            types = types.split(',')

            for type_name in types:
                type_name = type_name.strip(' ')
                type_name_id = Type.objects.get(name = type_name).id

                category_id = Category.objects.get(
                    menu_id = menu_id,
                    type_name_id = type_name_id
                ).id

                if not ProductCategory.objects.filter(
                    product_id = product_id,
                    category_id = category_id
                    ).exists():
                    # print(product_id, category_id)
                    ProductCategory.objects.create(
                        product_id = product_id,
                        category_id = category_id
                    )

def insert_tag():
    with open(CSV_PATH_TOTAL) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:
            tags = row[3]
            tags = tags.split(',')
            for tag in tags:
                tag_name = tag.strip('[]"\' ')
                
                if not Tag.objects.filter(name = tag_name).exists():
                    Tag.objects.create(name = tag_name)

def insert_product_tag():
    with open(CSV_PATH_TOTAL) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:

            product_name_ko = row[4]
            product_id = Product.objects.get(name_ko = product_name_ko).id

            tags = row[3]
            tags = tags.split(',')
            for tag in tags:
                tag_name = tag.strip('[]"\' ')
                tag_id = Tag.objects.get(name = tag_name).id

                if not ProductTag.objects.filter(
                    product_id = product_id,
                    tag_id = tag_id
                    ).exists():
                    ProductTag.objects.create(
                        product_id = product_id,
                        tag_id = tag_id
                    )

def insert_image():
    with open(CSV_PATH_TOTAL) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:

            product_name_ko = row[4]
            product_id = Product.objects.get(name_ko = product_name_ko).id

            images = row[9]
            images = images.split(',')

            for image in images:
                image_url = image.strip('[]"\' ')

                if not Image.objects.filter(
                    product_id = product_id,
                    image_url = image_url
                    ).exists():
                    # print(product_id, image_url)
                    Image.objects.create(
                        product_id = product_id,
                        image_url = image_url
                    )

def insert_series():
    with open(CSV_PATH_TOTAL) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:

            series = row[0]
            
            if not Series.objects.filter(series = series).exists():
                Series.objects.create(series = series)

def insert_product_series():
    with open(CSV_PATH_TOTAL) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:

            step = row[2]

            product_name = row[1]
            if not Product.objects.filter(name_ko = product_name):
                continue
            else:
                product_id = Product.objects.get(name_ko = product_name).id


            series = row[0]
            series_id = Series.objects.get(series = series).id

            if not ProductSeries.objects.filter(
                step = step,
                product_id = product_id,
                series_id = series_id
                ).exists():
                # print(step, product_id, series_id)
                ProductSeries.objects.create(
                    step = step,
                    product_id = product_id,
                    series_id = series_id
                )



#insert_product()
#insert_product_categories()
#insert_tag()
# insert_product_tag()
# insert_image()
# insert_series()
# insert_product_series()