from django.db import models

class Subscriber(models.Model):#класс подписчик
    email = models.EmailField()#поле для e-mail
    name = models.CharField(max_length=128)#поле для имени

    def __str__(self):
            return "Пользователь %s %s" % (self.name, self.email)

    class Meta:
        verbose_name = 'MySubscriber'
        verbose_name_plural = 'A lot of Subscribers'

