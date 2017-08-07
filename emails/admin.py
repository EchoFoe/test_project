from django.contrib import admin
from .models import *

admin.site.register(EmailType)

class EmailSendingFactAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EmailSendingFact._meta.fields]
    list_filter = ['email','type__name']
    search_fields = ['email','type__name']

    class Meta:
        model = EmailSendingFact

admin.site.register(EmailSendingFact,EmailSendingFactAdmin)