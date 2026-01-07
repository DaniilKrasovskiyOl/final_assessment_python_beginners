import re
import Table_methods


class Employee:
    # Храним все когда-либо использованные значения 'emp_id'
    used_ids = set()

    # Конструктор класса
    def __init__(self, emp_id, name , position, salary, email):
        if emp_id in self.used_ids:
            # Если значение уже использовалось, бросаем исключение
            raise ValueError(f"ID {emp_id} уже используется. Атрибут ID должен быть уникальными.")
        else:
            # Добавляем новое уникальное ID в множество
            self.used_ids.add(emp_id)
            self._emp_id = emp_id

            if not isinstance(name, str) or not name:
                raise ValueError("Имя сотрудника должно быть непустой строкой!")
            self._name  = name #имя сотрудника

            if not isinstance(position, str) or not position:
                raise ValueError("Должность сотрудника должна быть непустой строкой!")
            self._position = position #должность сотрудника

            if not isinstance(salary, float) or not salary or salary <= 0:
                raise ValueError("Зарплата сотрудника должна быть непустым положительным числом!")
            self._salary = salary #зарплата сотрудника

            if not isinstance(email, str) or not email:
                raise ValueError("Электронная почта сотрудника должна быть непустой строкой!")
            self._email = email #электронная почта сотрудника

            self._hours_worked = 0 #отработанное время в часах(по умолчанию 0)

            Table_methods.create_new_employee(self)

    # Метод добавляет отработанные часы
    def add_hours(self, hours):
        if hours <= 0:
            print("Значение отработанных часов должно быть больше 0!")
        else:
            self._hours_worked += hours
            Table_methods.update_employee_field(self._emp_id, 'Hours_worked', self._hours_worked)

    # Метод возвращает зарплату на основе отработанных часов, считая ставку как месячную зарплату, делённую на 160 часов
    def calculate_pay(self):
        return (self._hours_worked * self._salary) / 160

    # Метод проверяет поле email у сотрудника, если там введён email, то возвращает его,
    # в ином случае возвращает сообщение "EMAIL сотрудника некорректен!"
    def extract_email(self):
        # Шаблон для проверки стандартного формата email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,63}$'

        if re.fullmatch(email_regex, self._email):
            return self._email
        else:
            return "EMAIL сотрудника некорректен!"

    # Метод для получения данных в виде списка для записи в CSV
    def to_csv_row(self):
        return [self._emp_id, self._name, self._position, self._salary, self._email, self._hours_worked]