from .models import PrivacyPolicy

def getting_privacy_policy(request):
    privacy_policy = PrivacyPolicy.objects.filter(is_active=True).last() #Ласт длает так, чтобы из несколько
    #  созданных использовалась последняя
    return locals()