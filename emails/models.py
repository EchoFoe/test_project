from django.db import models

class EmailType(models.Model):
    name = models.CharField(max_length=64,blank=True,null=True,default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Тип е-мейла'
        verbose_name_plural = 'Типы е-мейлов'

class EmailSendingFact (models.Model):
    type = models.ForeignKey(EmailType, on_delete=models.CASCADE)
    order = models.ForeignKey("orders.Order", blank=True, null=True, default=None, on_delete=models.CASCADE)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.type.name

    class Meta:
        verbose_name = 'Отправленный е-мейл'
        verbose_name_plural = 'Отправленные е-мейлы'


