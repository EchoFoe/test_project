from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from test_project.settings import FROM_EMAIL, EMAIL_ADMIN
from emails.models import EmailSendingFact
from django.forms.models import model_to_dict


class SendingEmail(object):
    from_email = "111 <%s>" % FROM_EMAIL
    reply_to_emails = [from_email]
    target_emails = []
    bcc_emails = []

    def sending_email (self, type_id, email=None, order=None):#уведомление по запросу (что угодно можно)
        global subject, message
        if not email:
            email = EMAIL_ADMIN

        target_emails = [email]

        vars = dict()#это словарь, который передается в хтмл шаблон (он внизу)
        if type_id == 1: #означает, что "если уведомление администратору, то:"
            subject = "Новый заказ"
            vars["order_fields"] = model_to_dict(order)#все поля в записи ЗАКАЗ эта функция конвертирует в словарь
            # и дальше можно на хтмл вытаскивать эти записи
            vars["order"] = order
            vars["products_in_order"] = order.productinorder_set.filter(is_active=True)#добавляются все
            # товары в заказ, которые не были отменены (True)
            message = get_template('emails_templates/order_notification_admin.html').render(vars)#хтмл шаблон
            # прилагается (админовский)

        elif type_id == 2:#означает, что если не админ, то покупателю уведомление пойдет следующее:
            subject = 'Ваш заказ в магазине "Neformat-inc" получен!'
            message = get_template('emails_templates/order_notification_customer.html').render(vars)#хтмл шаблон
            # прилагается (для заказчика)

        msg = EmailMessage(subject, message, from_email=self.from_email, to=target_emails, bcc=self.bcc_emails, reply_to=self.reply_to_emails) #по стандарту есть либа "е-майл месадж" (она вверху)
        msg.content_subtype = 'html'
        msg.mixed_subtype = 'related'
        msg.send()

        kwargs = {
            "type_id": type_id,
            "email": email
        } #создаем словарь и добавляем в него нужные нам поля, а именно тип айди и е-майл
        if order: #если есть заказы, то:
            kwargs["order"] = order #добавляется поле заказа
        EmailSendingFact.objects.create(**kwargs)#создаем запись этой модели с помощью словаря, который выше

        print('Email was sent succesfully!')