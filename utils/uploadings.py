import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))
import django
django.setup()
from products.models import Product
import xlrd


class UploadingProducts(object):
    foreign_key_fields = ["category"]
    model = Product

    def __init__(self, data):#Когда вызывается класс, тогда и вызывается эта функция
        #  и передаем словарь - uploading_file = UploadingProducts({"file": file})
        data = data#через дата словарь считывается
        self.uploaded_file = data.get("file")
        self.parsing()

    def getting_related_model(self, field_name):
        model = self.model
        related_model = model._meta.get_field(field_name).rel.to
        return related_model

    def getting_headers(self):
        s = self.s #Лист уже висит в памяти (смотреть ниже)
        headers = dict()
        for column in range(s.ncols):#для колонки из диапазона колонок считываем сколько
            # колонок есть в полученном листе (динамически определяет число колонок в листе иксель)
            value = s.cell(0, column).value# cell это ячейка, а 0, потому что берем заголовок файла.
            headers[column] = value#для колонки, которую мы вытащили, записываем название
        return headers

    def parsing(self):#Функция парсинг считывает файл, который висит в классе uploaded_file
        uploaded_file = self.uploaded_file
        wb = xlrd.open_workbook(file_contents=uploaded_file.read())#открываем этот файл
        s = wb.sheet_by_index(0)#эта конструкция открывает первый лист в икселевском файле (0) - это первый лист
        self.s = s#s - записываем сюда значение этого листа

        headers = self.getting_headers()#Получаем заголовки этого листа
        print(headers)

        product_bulk_list = list()
        for row in range (1, s.nrows):#для строчки из диапазона строчек считываем сколько
            # строчек есть в полученном листе (динамически определяет число строчек в листе иксель)
            row_dict = {}
            for column in range (s.ncols):# когда заходим в каждую строку, то проходимся и по колонкам!
                value = s.cell(row, column).value# считываем текущее значение ячейки для каждой
                # строки для каждой колонки
                field_name = headers[column]#есть словарь хэдерс и подставляем индекс
                # колонки и получаем в ответ название поля field_name

                if field_name == "id" and not value:
                    continue

                if field_name in self.foreign_key_fields:
                    related_model = self.getting_related_model(field_name)
                    print(related_model)

                    instance, created = related_model.objects.get_or_create(name=value)
                    value = instance

                row_dict[field_name]=value

            print(row_dict)
            product_bulk_list.append(Product(**row_dict))
            # Product.objects.create(**row_dict)

        Product.objects.bulk_create(product_bulk_list)
        return True