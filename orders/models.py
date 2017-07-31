from django.db import models
from products.models import Product
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Status(models.Model):#поле статуса
    name = models.CharField(max_length=24)#имя поля
    is_active = models.BooleanField(default=True)#'активный/неактивный статус'
    created = models.DateTimeField(auto_now_add=True, auto_now=False)#поле авто даты создания заказа
    updated = models.DateTimeField(auto_now_add=True, auto_now=False)#поле авто даты обновления заказа
    def __str__(self):
            return "Статус %s" % (self.name)#возвращает по айди и имени
    class Meta:
        verbose_name = 'Статус заказа'#в единственном числе поле
        verbose_name_plural = 'Статусы заказа'# в множественном числе поле

class Order(models.Model):#класс заказ
    user = models.ForeignKey(User, null=True, default=None)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)#общая цена заказа в продуктах
    customer_name = models.CharField(max_length=128, blank=True, null=True, default=True)#поле для имени заказчика
    customer_email = models.EmailField(blank=True, null=True, default=True)#поле для e-mail заказчика
    customer_phone = models.CharField(max_length=68, blank=True, null=True, default=True)#поле для телефона заказчика
    customer_address = models.CharField(max_length=128, blank=True, null=True, default=None)#поле для адресса заказчика
    comments = models.TextField(blank=True, null=True, default=None)#поле для комментариев
    Status = models.ForeignKey(Status)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)#поле авто даты создания заказа
    updated = models.DateTimeField(auto_now_add=True, auto_now=False)#поле авто даты обновления заказа
    def __str__(self):
            return "Заказ %s %s" % (self.id, self.Status.name)#возвращает по айди и имени

    class Meta:
        verbose_name = 'Заказ'#в единственном числе поле
        verbose_name_plural = 'Заказы'# в множественном числе поле

    def save(self, *args, **kwargs):
            super(Order, self).save(*args, **kwargs)

class ProductInOrder(models.Model):#класс товар (в заказе)
    order = models.ForeignKey(Order, blank=True, null=True, default=None)#поле заказ
    product = models.ForeignKey(Product, blank=True, null=True, default=None)#поле продукт
    nmb = models.IntegerField(default=True)#поле для номер
    price_per_item = models.DecimalField(max_digits=10,decimal_places=2, default=0)#поле для цены за единицу товара
    total_price = models.DecimalField(max_digits=10,decimal_places=2, default=0)#поле для цена*продукт
    is_active = models.BooleanField(default=True)#поле активности/неактивности
    created = models.DateTimeField(auto_now_add=True, auto_now=False)#поле авто даты заказа
    updated = models.DateTimeField(auto_now_add=True, auto_now=False)#поле авто даты обновления заказа
    def __str__(self):
            return "%s" % (self.product.name)

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def save(self, *args, **kwargs):
            price_per_item = self.product.price
            self.price_per_item = price_per_item
            print(self.nmb)
            self.total_price = int(self.nmb) * self.price_per_item
            super(ProductInOrder, self).save(*args, **kwargs)

def product_in_order_post_save (sender, instance, created, **kwargs):

    order = instance.order
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

    order_total_price = 0
    for item in all_products_in_order:
        order_total_price += item.total_price

    instance.order.total_price = order_total_price
    instance.order.save(force_update=True)

post_save.connect(product_in_order_post_save, sender=ProductInOrder)


class ProductInBasket(models.Model):#класс товар (в корзине)
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
    order = models.ForeignKey(Order, blank=True, null=True, default=None)#поле заказ
    product = models.ForeignKey(Product, blank=True, null=True, default=None)#поле продукт
    nmb = models.IntegerField(default=True)#поле для номер
    price_per_item = models.DecimalField(max_digits=10,decimal_places=2, default=0)#поле для цены за единицу товара
    total_price = models.DecimalField(max_digits=10,decimal_places=2, default=0)#поле для цена*продукт
    is_active = models.BooleanField(default=True)#поле активности/неактивности
    created = models.DateTimeField(auto_now_add=True, auto_now=False)#поле авто даты заказа
    updated = models.DateTimeField(auto_now_add=True, auto_now=False)#поле авто даты обновления заказа
    def __str__(self):
            return "%s" % (self.product.name)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
            price_per_item = self.product.price
            self.price_per_item = price_per_item

            self.total_price = int (self.nmb) * price_per_item
            super(ProductInBasket, self).save(*args, **kwargs)