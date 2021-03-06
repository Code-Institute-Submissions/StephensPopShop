from django.db import models

# Create your models here.
class Product(models.Model):
    BLEACH = 'Bleach'
    DRAGONBALLZ = 'DragonballZ'
    SWORDARTONLINE = 'Sword Art Online'
    
    SERIES_CHOICES = (
        (BLEACH, 'Bleach'),
        (DRAGONBALLZ, 'Dragonballz'),
        (SWORDARTONLINE, 'Sword Art Online'),
        )


    name = models.CharField(max_length=254, default= '')
    description = models.TextField(max_length=270)
    original_item_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    instant_buy_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    image = models.ImageField(upload_to='images/',
                             width_field="width_field",
                             height_field="height_field",
                             default='default.png')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    series = models.CharField(max_length=16, choices=SERIES_CHOICES, default= '')
    character = models.CharField(max_length=200, default= '')
    

    def __str__(self):
        return self.name
