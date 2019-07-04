from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .models import*
from django.shortcuts import render
from .forms import CheckoutContactForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Count, Prefetch, Sum

from itertools import chain
from operator import itemgetter
from utils.emails import SendingEmail
from django.db.models.functions import TruncDate, TruncMonth
import json
from decimal import Decimal
from datetime import date, datetime




def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    print (request.POST)
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    is_delete = data.get("is_delete")

    if is_delete == 'true':
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id,
                                                                     is_active=True, order=None, defaults={"nmb": nmb})
        if not created:
            print ("not created")
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)

    #common code for 2 cases
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb

    return_dict["products"] = list()

    for item in  products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.id
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = item.nmb
        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)


def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    print(products_in_basket)
    for item in products_in_basket:
        print(item.order)

    # Форма для заполнения информации о контакте

    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        print(request.POST)
        if form.is_valid():
            print("yes")
            data = request.POST
            name = data.get("name", "3423453")
            phone = data["phone"]
            email = data.get("email")
            user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name, "email": email})

            order = Order.objects.create(user=user, customer_name=name, customer_phone=phone,
                                         customer_email=email, Status_id=1)#создаем заказ

            for name, value in data.items():#проходимся по товарам в КОРЗИНЕ
                if name.startswith("product_in_basket_"):
                    product_in_basket_id = name.split("product_in_basket_")[1]
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
                    print(type(value))

                    product_in_basket.nmb = value
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)

                    ProductInOrder.objects.create(product=product_in_basket.product, nmb = product_in_basket.nmb,
                                                  price_per_item=product_in_basket.price_per_item,
                                                  total_price = product_in_basket.total_price,
                                                  order=product_in_basket.order)
                    #для каждого ТОВАРА создаем запись в таблице и коннектим наш ЗАКАЗ
            # sending notifications emails
            email = SendingEmail()
            email.sending_email(type_id=1, order=order)
            email.sending_email(type_id=2, email=order.customer_email, order=order)
            
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            print("no")
    return render(request, 'orders/checkout.html', locals())

def repairs (request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    print(products_in_basket)
    for item in products_in_basket:
        print(item.order)

    # Форма для заполнения информации о контакте

    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        print(request.POST)
        if form.is_valid():
            print("yes")
            data = request.POST
            name = data.get("name", "3423453")
            phone = data["phone"]
            user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name})

            order = Order.objects.create(user=user, customer_name=name, customer_phone=phone, Status_id=1)

            for name, value in data.items():
                if name.startswith("product_in_basket_"):
                    product_in_basket_id = name.split("product_in_basket_")[1]
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
                    print(type(value))

                    product_in_basket.nmb = value
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)

                    ProductInOrder.objects.create(product=product_in_basket.product, nmb = product_in_basket.nmb,
                                                  price_per_item=product_in_basket.price_per_item,
                                                  total_price = product_in_basket.total_price,
                                                  order=order)#order = product_in_basket.order


            #sending notifications emails
            email = SendingEmail()
            email.sending_email(type_id = 1, order=order)
            email.sending_email(type_id = 2, email=order.customer_email, order=order)

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            print("no")
    return render(request, 'orders/repairs.html', locals())

def admin_orders(request):

    user = request.user
    if user.is_superuser:

        orders = Order.objects.all().annotate(products_nmb = Count('productinorder'))\
            .values()#отображение всех заказов, а вэльюс можно перечислять поля, которые нам нужны
        order_ids = [order["id"] for order in orders]

        products_in_order = ProductInOrder.objects.filter(is_active=True, order_id__in=order_ids)\
            .values("order_id","product__name","nmb","price_per_item","total_price", "order__Status__name")

        def merging_dicts(l1, l2, key1, key2):#делаем словарь
            merged={}
            for item in l1:#проходимся по всем словарям в списке 1(l1)
                merged[item[key1]]=item#ключ 1 это "id" заказа
            for item in l2:
                try:
                    if "products" in merged [item[key2]]:
                        merged[item[key2]]["products"].append(item)#ключ 2 это "order_id" товаров в заказе
                    else:
                        merged[item[key2]]["products"]=[item]

                except Exception as e:
                    return True

            orders = [val for (_, val) in merged.items()]
            return orders
        orders = merging_dicts(list(orders), list(products_in_order), "id", "order_id")
        #передае в виде списка товары в заказе и по какому полю их сравнивать ( айди, ордер_айди)
        return render(request, 'orders/admin_orders.html', locals())
    else:
        return HttpResponseRedirect(reversed("home"))

def dashboard(request):
    #1ый график, который отражает кол-во заказов во времени id="container_1"
    user = request.user
    if not user.is_superuser:
        return HttpResponseRedirect(reverse("home"))#Если юзер не супер юзер, то делаем редирект домой

    all_orders_by_dates = Order.objects.all()\
        .annotate(date_item=TruncDate('created'))\
        .values("date_item", "Status__name", "Status_id")\
        .annotate(orders_amount = Sum ("total_price"))\
        .order_by("date_item")
    #к каждой записи добавляю поле date_item которое содержит значение TruncDate('created')\
    #из всех полей в заказе мне НЕОБХОДИМО поле date_item, status__name, status_id\
    #к каждой записи с полями (что выше) добавляю поле общая цена заказа для каждой группы\
    #сортируется весь этот список по дате - date_item

    dates_list = list()
    all_orders_by_dates_dict = dict()
    cancelled_orders_by_dates_dict = dict()

    for order_by_dates in all_orders_by_dates:
        if not order_by_dates["date_item"] in dates_list:
            dates_list.append(order_by_dates["date_item"])

        if order_by_dates["date_item"] in all_orders_by_dates_dict:
            all_orders_by_dates_dict[order_by_dates["date_item"]] += order_by_dates["orders_amount"]
        else:
            all_orders_by_dates_dict[order_by_dates["date_item"]] = order_by_dates["orders_amount"]
        #Если в этом словаре есть дата, тогда выбираем запись по этой же дате  и к тому значение, которое уже есть
        #добавляется (+=) к существующему значению еще значение orders_amount
        #иначе:
        #просто создаем итерейшн из цикла, т.е. order_by_dates["orders_amount"]

        if order_by_dates["Status_id"] == 4:
            if order_by_dates["date_item"] in cancelled_orders_by_dates_dict:
                cancelled_orders_by_dates_dict [order_by_dates["date_item"]] += order_by_dates["orders_amount"]
            else:
                cancelled_orders_by_dates_dict[order_by_dates["date_item"]] = order_by_dates["orders_amount"]
        # Если в этом словаре есть дата, тогда выбираем запись по этой же дате  и к тому значение, которое уже есть
        # добавляется к существующему значению orders_amount, только уже по ОТМЕНЕННОМУ ЗАКАЗУ (["status_id"] == 3)
        # иначе:
        # просто создаем итерейшн из цикла, т.е. order_by_dates["orders_amount"]

    all_orders_by_dates_data = list()
    for date_item in dates_list:
        if date_item in all_orders_by_dates_dict:
            all_orders_by_dates_data.append(all_orders_by_dates_dict[date_item])
        else:
            all_orders_by_dates_data.append(0)
    # Проходим по списку дат date_item
    # и смотрим ЕСЛИ эта дата есть в словаре all_orders_by_dates_dict, то делаем append
    # иначе:
    # append(0)

    cancelled_orders_by_dates_data = list()
    for date_item in dates_list:
        if date_item in cancelled_orders_by_dates_dict:
            cancelled_orders_by_dates_data.append(cancelled_orders_by_dates_dict[date_item])
        else:
            cancelled_orders_by_dates_data.append(0)
    #такая же логика и для отмененных товаров

    charts_data = dict()
    charts_data["chart_orders"] = dict()
    charts_data["chart_orders"]["dates_list"] = dates_list
    charts_data["chart_orders"]["series"] = [
        {"name": "все заказы", "data": all_orders_by_dates_data},
        {"name": "отмененные заказы", "data": cancelled_orders_by_dates_data}
    ]
    # объявляем переменную charts_data
    # добавляем ключ словаря chart_orders - график с заказами
    # в этот график с заказами добавляем ключ dates_list - список дат
    # добавляем ключ series, где содержатся две ЛИНИИ графика в качестве словарей all_orders_by_dates_data
                                                                        # и cancelled_orders_by_dates_data

    #2ой график, который отражает кол-во заказов по продуктам id="container_2"
    products_in_orders_by_dates = ProductInOrder.objects.all()\
        .annotate(date_item=TruncDate('created'))\
        .values("date_item", "product__name")\
        .annotate(orders_amount=Sum("total_price"))\
        .order_by("date_item")
    # достаются все товары в заказе (и дальше по аналогии, как выше)

    products_in_orders_by_dates_dict = dict()
    for product_in_orders in products_in_orders_by_dates:
        if product_in_orders["product__name"] in products_in_orders_by_dates_dict:
            products_in_orders_by_dates_dict[product_in_orders["product__name"]][product_in_orders["date_item"]]\
                = product_in_orders["orders_amount"]
        else:
            products_in_orders_by_dates_dict[product_in_orders["product__name"]] = {
                product_in_orders["date_item"]:product_in_orders["orders_amount"]
            }
    # делается словарь, в котором ключом является product__name, а значения являются orders_amount - продажи
    # но тут не будет фильтрации товара по статусу!

    charts_data["chart_products_in_orders"] = dict()
    charts_data["chart_products_in_orders"]["dates_list"] = dates_list
    # добавляем новый ключ для переменной charts_data - chart_products_in_orders и добавляем dates_list
    charts_data["chart_products_in_orders"]["series"] = []
    # так же добавляем ключ series
    for product, data in products_in_orders_by_dates_dict.items():

        data_list = list()
        for item_date in dates_list:
            data_value = data.get(item_date, 0)
            data_list.append(data_value)

        charts_data["chart_products_in_orders"]["series"]\
            .append({"name": product, "data": data_list})
    # проходимся по словарю products_in_orders_by_dates_dict
    # и добавляется charts_data "name" и "data" в виде списка, где берется только value

    def custom_serializer(obj):
        if isinstance(obj, (datetime, date)):
            serial = obj.isoformat()
            return serial
        if isinstance(obj, Decimal):
            return float(obj)

    charts_data = json.dumps(charts_data, default=custom_serializer)# переделываем набор словарей в формат json
    return render(request, 'orders/dashboard.html', locals())
