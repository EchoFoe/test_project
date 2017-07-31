from django.db import models
from django.template.defaultfilters import truncatechars
import PIL as pillow



class ProductCategory(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True, default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % self.name  # отображение по имени

    class Meta:
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категория товаров'

class Product(models.Model):#поле для продукта

    name = models.CharField(max_length=128, blank=True, null=True, default=True)#имя для продукта
    price = models.DecimalField(max_digits=10, decimal_places=2, default=True)  # поле для цена
    discount = models.IntegerField(default=0)# поле для скидки
    price_with_discount = models.DecimalField(max_digits=10, decimal_places=2, default=True)
    category = models.ForeignKey(ProductCategory, blank=True, null=True, default=True)
    short_description = models.TextField(max_length=50, blank=True, null=True, default=None,)  # краткое описание для продукта
    description = models.TextField(blank=True, null=True, default=None)#описание для продукта
    is_active = models.BooleanField(default=True)#активность/неактивность проудкта
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=True, auto_now=False)

    def price_discount(self, *args, **kwargs):
        self.price_with_discount = self.discount * self.price * 0.01
        # super(Product, self).save(*args, **kwargs)
        return (self.price_with_discount)

    def description_S(self):
        return truncatechars(self.description, 30)
    def __str__(self):
            return "%s (%s)" % (self.name, self.price)#отображение по имени


    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class ProductImage(models.Model):#класс фотография
    Product = models.ForeignKey(Product, blank=True, null=True, default=None)#поле для продукта
    image = models.ImageField(upload_to='products_images/')#директория для фотографии продукта
    is_main = models.BooleanField(default=False)  # активность/неактивность товара
    is_active = models.BooleanField(default=True)#активность/неактивность товара
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=True, auto_now=False)
    def __str__(self):
            return "%s" % (self.id)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'


class ForRepairsCategory(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True, default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % self.name  # отображение по имени

    class Meta:
        verbose_name = 'Категория ремонта'
        verbose_name_plural = 'Категория ремонтов'

class ForRepairs(models.Model):#поле для ремонта

    name = models.CharField(max_length=128, blank=True, null=True, default=True)#именной тэг для ремонта
    price = models.DecimalField(max_digits=10, decimal_places=2, default=True)  #цена для ремонта
    discount = models.IntegerField(default=0)# поле для скидки
    price_with_discount = models.DecimalField(max_digits=10, decimal_places=2, default=True)
    category = models.ForeignKey(ForRepairsCategory, blank=True, null=True, default=True)
    short_description = models.TextField(max_length=50, blank=True, null=True, default=None,)#краткое описание для продукта
    description = models.TextField(blank=True, null=True, default=None)#описание для продукта
    is_active = models.BooleanField(default=True)#активность/неактивность проудкта
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=True, auto_now=False)

    def price_discount(self, *args, **kwargs):
        self.price_with_discount = self.discount * self.price * 0.01
        # super(Product, self).save(*args, **kwargs)
        return (self.price_with_discount)

    def description_S(self):
        return truncatechars(self.description, 30)
    def __str__(self):
            return "%s (%s)" % (self.name, self.price)#отображение по имени


    class Meta:
        verbose_name = 'Для ремонта'
        verbose_name_plural = 'Для ремонта'

# class ForRepairsImage(models.Model):#класс фотография
#     Product = models.ForeignKey(Product, blank=True, null=True, default=None)#поле для продукта
#     image = models.ImageField(upload_to='products_images/')#директория для фотографии продукта
#     is_main = models.BooleanField(default=False)  # активность/неактивность товара
#     is_active = models.BooleanField(default=True)#активность/неактивность товара
#     created = models.DateTimeField(auto_now_add=True, auto_now=False)
#     updated = models.DateTimeField(auto_now_add=True, auto_now=False)
#     def __str__(self):
#             return "%s" % (self.id)
#
#     class Meta:
#         verbose_name = 'Фотография ремонт'
#         verbose_name_plural = 'Фотографии ремонт'