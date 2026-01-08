import re


class Employee:

    # Конструктор класса
    def __init__(self, emp_id, name, position, salary, email, hours_worked=0):
        # Добавляем новое уникальное ID в множество
        self.emp_id = int(emp_id)

        if not isinstance(name, str) or not name:
            raise ValueError("Имя сотрудника должно быть непустой строкой!")
        self.name = name  # имя сотрудника

        if not isinstance(position, str) or not position:
            raise ValueError("Должность сотрудника должна быть непустой строкой!")
        self.position = position  # должность сотрудника

        if not isinstance(salary, float) or not salary or salary <= 0:
            raise ValueError("Зарплата сотрудника должна быть непустым положительным числом!")
        self.salary = salary  # зарплата сотрудника

        if not isinstance(email, str) or not email:
            raise ValueError("Электронная почта сотрудника должна быть непустой строкой!")
        self.email = email  # электронная почта сотрудника

        self.hours_worked = int(hours_worked)  # отработанное время в часах(по умолчанию 0)

    # Метод добавляет отработанные часы
    def add_hours(self, hours):
        if hours <= 0:
            print("Значение отработанных часов должно быть больше 0!")
        else:
            self.hours_worked += hours
            return self.hours_worked

    # Метод возвращает зарплату на основе отработанных часов, считая ставку как месячную зарплату, делённую на 160 часов
    def calculate_pay(self):
        if self.hours_worked > 160:
            return self.salary + ((self.hours_worked - 160) * self.salary) / 80
        else:
            return (self.hours_worked * self.salary) / 160

    # Метод проверяет поле email у сотрудника, если там введён email, то возвращает его,
    # в ином случае возвращает сообщение "EMAIL сотрудника некорректен!"
    def extract_email(self):
        # Шаблон для проверки стандартного формата email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,63}$'

        if re.fullmatch(email_regex, self.email):
            return self.email
        else:
            return "EMAIL сотрудника некорректен!"
