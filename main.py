from fake_useragent import UserAgent
from bs4 import BeautifulSoup, Tag
from typing import List
from all_classes import Vacanсy
from custom_exception import EmptyVacancy
from contextlib import suppress
from httpx import Response
from tqdm import tqdm
import httpx
import time

def create_query(number_page: int = 1) -> Response:
    """
    Функция генерирует запрос на страницу

    number_page: int
        Номер страницы запроса

    return: Response
        Возвращает ответ интернет ресурса
    """
    ua = UserAgent().googlechrome

    url = "https://smolensk.hh.ru/search/vacancy"
    param = {
        "L_save_area": "true",
        "search_field": "name",
        "search_field": "description",
        "area": "1",
        "schedule": ["fullDay", "shift", "remote"],
        # "schedule": "shift",
        # "schedule": "remote",
        "search_period": "30",
        "items_on_page": "50",
        "hhtmFrom": "vacancy_search_filter",
        "experience": "between1And3",
        "professional_role": "96",
        "text": "Python",
        "page": str(number_page),
        "enable_snippets": "false"
        }
    head = {"user-agent": ua}

    response = httpx.get(url=url,
                         params=param,
                         headers=head)

    if response.status_code != 200:
        raise Exception
    
    return response
    

def parser_max_page(element: BeautifulSoup) -> int:
    """
    Функция считывает кол-во страниц которые надо спарсить

    element: BeautifulSoup
    Класс для парсинга HTML странички

    return: int
        Возвращает максимальный номер страницы
    """
    query_name = {
            "data-qa": "pager-page"
            }

    name_pars = element.find_all(name="a", class_="bloko-button", rel="nofollow", attrs=query_name)

    list_page = list()
    for i_elem in name_pars:
        list_page.append(int(i_elem.span.text))

    return max(list_page) - 1


def count_elem_in_page(element: BeautifulSoup) -> List[Tag]:
    """
    Функция находит нужные элементы на страницы и возвращает список

    element: BeautifulSoup
        Класс для парсинга HTML странички

    return: List[Tag]
        Возвращает список найденных элементов
    """
    res: List[Tag] = element.find_all(name="a", class_="bloko-link", target="_blank")

    return res



def main() -> None:
    "Руководящая функция"

    # Делаем запрос и проверяем сколько надо спарсить страниц
    response = create_query()
    soup = BeautifulSoup(response.text, "html.parser")
    count_page = parser_max_page(element=soup)
    all_element = list()

    print("Подсчитываем сложность поиска...\n   Заварите чайку\n")

    # Находим все нужные элементы на страницы и добавляем  список
    for i_elem in range(1, count_page):
        time.sleep(5)
        query = create_query(i_elem)
        soup = BeautifulSoup(query.text, "html.parser")
        all_element.extend(count_elem_in_page(element=soup))
        
    print("А я говорил завари чайку)))\n\n")

    # Выполняется парсинг страницы с прогресс баром
    for i_elem in tqdm(all_element):
        time.sleep(5)
        pars_vacansiy = Vacanсy(url=i_elem["href"])
        pars_vacansiy()

        # Записываем результат в файл
        with suppress(EmptyVacancy):
            with open("all_vacansii.txt", mode="a") as work_file:
                    work_file.write(pars_vacansiy.for_write())
             

if __name__ == "__main__":
    main()
