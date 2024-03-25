from typing import Any, Optional, List
from fake_useragent import UserAgent
from bs4 import BeautifulSoup, PageElement
from httpx import Response
from custom_exception import EmptyVacansiy
import httpx 



class Vacansiy:
    "Класс описывает вакансию которую спарсил"

    def __init__(self,
                 url: str,
                 name: Optional[str] = None,
                 salary: Optional[str] = None
                 ) -> None:
        """
        Метод для создания экземпляра

        url: str
            Страница вакансии (url-адресс)

        name: Optional[str]
            Название вакансии

        salary: Optional[str]
            Зарплата вакансии
        """

        self.url = url
        self.name = name
        self.salary = name


    def __call__(self, *args: Any, **kwds: Any) -> Any:
        """
        Метод вызова класса который находит нужные 
        элементы на странице вакансии
        """
        answer = self.creata_query()
        if answer is None:
            return self
        
        new_name = self.parsing_page_name(response=answer)
        new_salary = self.parsing_page_salary(response=answer)

        self.name = new_name
        self.salary = new_salary

        return self

    @staticmethod
    def convert_string(tags: List[PageElement]) -> str:
        """
        Метод соединяет строки из элементов

        tags: List[PageElement]
            Список элементов для имени

        return: str
            Возвращает строку
        """
        if len(tags) == 1:
            return tags[0].text

        futury_name = str()
        for i_elem in tags:
            futury_name += i_elem.text

        return futury_name


    def parsing_page_salary(self, response: Response) -> str | None:
        """
        Методв ищет зарплату вакансии на странице

        response: Response
            Ответ интернет русурса

        return: str
            Возвращает зарплату вакансии
        """
        
        query_salary = {
            "data-qa": "vacancy-salary"
            }
        soup = BeautifulSoup(response.text, "html.parser")
        salary_pars = soup.find(name="div", attrs=query_salary)

        if salary_pars is not None:
            new_salary = self.convert_string(tags=salary_pars.contents) # type: ignore

        else:
            new_salary = None
        
        return new_salary
                

    def parsing_page_name(self, response: Response) -> str:
        """
        Метод ищет название вакансии на странице

        response: Response
            Ответ интернет ресурса

        return: str
            Возвращает название вакансии
        """

        query_name = {
            "data-qa": "vacancy-title"
            }

        soup = BeautifulSoup(response.text, "html.parser")
        name_pars = soup.find(name="h1", class_="bloko-header-section-1", attrs=query_name)
        new_name = self.convert_string(tags=name_pars.contents) # type: ignore

        return new_name

    
    def creata_query(self) -> Response |  None:
        """
        Метод создает запрос и проверяет какие коды пришли

        return: Response | None
            Response - Возвращает ответ интернет ресурса
            None - Если ресурс ничего не содержит
        """

        ua = UserAgent().googlechrome
        head = {"user-agent": ua}
        response = httpx.get(url=self.url, headers=head)

        match response.status_code:
            case 301: # Ресурс ничего не содержит
                return None
            
            case 302: # Перенаправление ресурса
                new_response = httpx.get(url=response.headers["location"], headers=head)
                return new_response 
            
            case 200: # Успешный ответ от ресурса
                return response


    def __str__(self) -> str:
        """
        Метод для отображения класса
        
        return: str
            Возвращает строковое представление класса
        """

        data = f"Вакансия: {self.name}\n" \
               f"Зарплата: {self.salary if self.salary is not None else 'Не указана'}\n" \
               f"URL: {self.url}\n\n"

        return data
    

    def for_write(self) -> str:
        """
        Метод возвращает строку для записи в файл или же вызывает исключение, если 
        нет название вакансии

        return: str
            Возвращает строку для записи в файл
        """

        if self.name is None:
            raise EmptyVacansiy(message="Вакансия пустая")
        
        data = f"Вакансия: {self.name}\n" \
               f"Зарплата: {self.salary if self.salary is not None else 'Не указана'}\n" \
               f"URL: {self.url}\n\n"

        return data