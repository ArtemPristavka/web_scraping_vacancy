

class EmptyVacansiy(Exception):
    "Класс ошибки, что вакансии не существует"
    
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message