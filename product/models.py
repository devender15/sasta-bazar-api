from django.db import models
import random, string


def generateUniqueProductId():

    # getting all type of characters for generating Id
    uppercaseArray = string.ascii_uppercase
    lowercaseArray = string.ascii_lowercase
    numbersArray = string.digits

    # we will add all the characters in this array using extend function
    completeComboArray = []

    completeComboArray.extend(uppercaseArray)
    completeComboArray.extend(lowercaseArray)
    completeComboArray.extend(numbersArray)

    # just changing the order of all the chars so that every time they will be different
    random.shuffle(completeComboArray)

    while 1:

        # here is the final unique id ( 30 characters long ) for our products
        productId = "".join(random.sample(completeComboArray, 30))

        # checking if our id is unique or not
        if(Product.objects.filter(productId=productId).count() == 0):
            break

    return productId



class MainCategory(models.TextChoices):
    MEN = 'men'
    WOMEN = 'women'
    KIDS = 'kids'
    MOBILES = 'mobiles'
    TECHNOLOGY = 'technology'
    DECORATION = 'decoration'
    KITCHEN = 'kitchen'

class SubCategory(models.TextChoices):
    NOT_SELECTED = 'Not Selected'
    UPPERCLOTHING = 'upperclothing'
    BOTTOMCLOTHING = 'bottomclothing'
    FOOTWEAR = 'footwear'
    ACCESSORIES = 'accessories'

class Product(models.Model):
    productId = models.CharField(max_length=35, default=generateUniqueProductId, unique=True)
    productName = models.CharField(max_length=200)
    category = models.CharField(max_length=25, choices=MainCategory.choices, default='')
    subCategory = models.CharField(max_length=20, null=True, choices=SubCategory.choices, blank=True, default=SubCategory.NOT_SELECTED)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=300)
    pubishDate = models.DateField()
    productImage = models.ImageField(upload_to="product/images", default="")

    def __str__(self):
        return self.productName