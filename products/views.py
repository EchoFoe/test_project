from django.shortcuts import render
from products.models import *
from utils.uploadings import UploadingProducts
from django.contrib import messages


def product(request, product_id):
    products = Product.objects.get(id=product_id)

    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    print(request.session.session_key)

    return render(request, 'products/product.html', locals())

def download_products(request):
    if request.POST:
        print(request.POST)
        print(request.FILES)
        file = request.FILES['file']#этот file прописан download_products.html
        uploading_file = UploadingProducts({"file": file})#потом файл передаем в класс UploadingProducts
        if uploading_file:
            messages.success(request, 'Успешная загрузка')#Этот нотификейшен отображается за счет
            # errors_notification.html - if 'succes' in message.tags
        else:
            messages.error(request, 'Ошибка при загрузке!')#Этот нотификейшен отображается за счет
            # errors_notification.html - if 'error' in message.tags
    return render(request, 'products/download_products.html', locals())

