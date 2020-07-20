
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
import json
import pandas as pd

page = 0

params = {'area': 1,
          'st': 'searchVacancy',
          'fromSearch': 'true',
          'text': 'Machine learning python',
          'page': page}

headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'}

main_link = 'https://hh.ru'
link_folder = '/search/vacancy'
response = requests.get(main_link + link_folder, headers=headers, params=params)
soup = bs(response.text,'lxml')

vacancies_block = soup.find('div', {'class': 'vacancy-serp'})
vacancies_list = vacancies_block.find_all('div', {'data-qa': 'vacancy-serp__vacancy', 'class': 'vacancy-serp-item'})
counter = 0

vacancies = []

for vacancy in vacancies_list:
    vacancy_data = {}
    vacancy_data['name'] = vacancy.find('a').getText()
    vacancy_data['vacancy_link'] = vacancy.find('a')['href']
    vacancy_data['employer_source'] = main_link + vacancy.find('a', {'class': 'bloko-link bloko-link_secondary', 'data-qa': 'vacancy-serp__vacancy-employer'})['href']
    vacancy_data['employer'] = vacancy.find('div', {'class': 'vacancy-serp-item__meta-info'}).getText()
    next_page = \
    soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control', 'data-qa': 'pager-next'})['href']
    salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText()
    max = re.search(r"(?<=до ).*?(?= )|(?<=-)\d*\s\d*", salary)
    min = re.search(r"(?<=от ).*?(?= )|.*?(?=-)", salary)
    curr = re.search(r".{4}$", salary)
    if max:
        vacancy_data['salary_max'] = max.group(0).replace('\xa0000', '')
    else:
        vacancy_data['salary_max'] = 'не указана'
    if min:
        vacancy_data['salary_min'] = min.group(0).replace('\xa0000', '')
    else:
        vacancy_data['salary_min'] = 'не указана'
    if curr:
        vacancy_data['salary_currency'] = curr.group(0)
    else:
        vacancy_data['salary_currency'] = 'не указана'
    vacancies.append(vacancy_data)


# min r"(?<=от ).*?(?= )|.*?(?=-)"
# max r"(?<=до ).*?(?= )|(?<=-)\d*\s\d*"

# max (?<=до ).*?(?=\s)|(?<=-).*?(?=\s)
# min (?<=от ).*?(?=\s)|.*?(?=\-)

