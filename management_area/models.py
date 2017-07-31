from django.db import models

class PrivacyPolicy(models.Model):
    text = models.TextField()
    is_active = models.BooleanField(default=True)#'активный/неактивный статус'
    created = models.DateTimeField(auto_now_add=True, auto_now=False)#поле авто даты создания заказа
    updated = models.DateTimeField(auto_now_add=True, auto_now=False)#поле авто даты обновления заказа

    def __str__(self):
            return "Статус %s" % (self.text)#возвращает по айди и имени
    class Meta:
        verbose_name = 'Политика конфиденциальности'#в единственном числе поле
        verbose_name_plural = 'Политики конфиденциальности'# в множественном числе поле