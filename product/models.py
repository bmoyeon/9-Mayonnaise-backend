from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = "menus"

class Type(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = "types"

class Category(models.Model):
    menu      = models.ForeignKey("Menu", on_delete = models.SET_NULL, null = True)
    type_name = models.ForeignKey("Type", on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = "categories"

class Product(models.Model):
    name_ko          = models.CharField(max_length = 200)
    name_en          = models.CharField(max_length = 200)
    description      = models.CharField(max_length = 1000)
    price            = models.DecimalField(max_digits = 10, decimal_places = 2)
    volume           = models.CharField(max_length = 50)
    ingredient       = models.CharField(max_length = 2000)
    feature          = models.TextField()
    categories       = models.ManyToManyField("Category", through = "ProductCategory")
    tags             = models.ManyToManyField("Tag", through = "ProductTag")
    series           = models.ManyToManyField("Series", through = "ProductSeries")

    class Meta:
        db_table = "products"

class ProductCategory(models.Model):
    product  = models.ForeignKey("Product", on_delete = models.SET_NULL, null = True)
    category = models.ForeignKey("Category", on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = "product_categories"

class Tag(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = "tags"

class ProductTag(models.Model):
    product = models.ForeignKey("Product", on_delete = models.SET_NULL, null = True)
    tag     = models.ForeignKey("Tag", on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = "product_tags"

class Series(models.Model):
    series = models.CharField(max_length = 50)

    class Meta:
        db_table = "series"

class ProductSeries(models.Model):
    step    = models.CharField(max_length = 50)
    product = models.ForeignKey("Product", on_delete = models.SET_NULL, null = True)
    series  = models.ForeignKey("Series", on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = "product_series"

class Image(models.Model):
    image_url   = models.URLField(max_length = 2000)
    product     = models.ForeignKey("Product", on_delete = models.SET_NULL, null = True)
    is_main_img = models.BooleanField(default = False)

    class Meta:
        db_table = "images"