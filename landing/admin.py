from django.contrib import admin
from .models import *

class SubscriberAdmin (admin.ModelAdmin):#класс подписчик
    list_display = [field.name for field in Subscriber._meta.fields]#отображение поля имени
    list_filter = ['name',]#фильтр по именам
    search_fields = ['name', 'email',]#поисковик по имени/e-mail

    # list_display = ["name", "email"]
    # inlines = [FileMappingInline]
    # fields = []
    # #exclude = ["type"]
    # #list_filter = ('report_data',)
    # search_fields = ['category','subCategory','suggestKeyword']

    class Meta:
        model = Subscriber
admin.site.register(Subscriber, SubscriberAdmin)
