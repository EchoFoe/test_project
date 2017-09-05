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
        file = request.FILES['file']
        uploading_file = UploadingProducts({"file": file})
        if uploading_file:
            messages.success(request, 'Успешная загрузка')
        else:
            messages.error(request, 'Ошибка при загрузке!')
    return render(request, 'products/download_products.html', locals())

