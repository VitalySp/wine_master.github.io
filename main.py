from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

import datetime

import pandas

import collections

from pprint import pprint


excel_data = pandas.read_excel('wine3.xlsx', sheet_name='Лист1', keep_default_na=False, usecols=['Категория','Название', 'Сорт', 'Цена', 'Картинка', 'Акция'])

excel_data_dict = excel_data.to_dict(orient='record')

def categorie_catalog(category_name):
    categorie_catalog = []
    for dic in excel_data_dict:
        for key, value in dic.items():
            if key == 'Категория' and value == category_name:
                categorie_catalog.append(dic)
    return categorie_catalog

def drinks_catalog():
    categorie_names = []

    for dic in excel_data_dict:
        for key, value in dic.items():
            if key == 'Категория' :
                categorie_names.append(value)
    category_names = sorted(set(categorie_names))
    
    drinks_catalog = collections.defaultdict(list)

    for category_name in category_names:
        drinks_catalog[category_name] = categorie_catalog(category_name)

    return drinks_catalog

drinks_catalog = drinks_catalog()

pprint(drinks_catalog)

present_time = datetime.datetime.now()

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    company_age=present_time.year - 1920,
    drinks_catalog=drinks_catalog,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
