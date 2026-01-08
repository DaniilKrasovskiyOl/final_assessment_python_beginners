import enum
from Employee import Employee
from typing import Optional


class TaskStatus(enum.Enum):
    IN_PROGRESS = "В процессе"
    FINISHED = "Завершено"


class Task:
    # Конструктор класса
    def __init__(self, task_id, title, description, status = TaskStatus.IN_PROGRESS.value):
        self.task_id = task_id
        if not isinstance(title, str) or not title:
            raise ValueError("Название задачи должно быть непустой строкой!")
        self.title = title  # название задачи

        if not isinstance(description, str) or not description:
            raise ValueError("Описание задачи должно быть непустой строкой!")
        self.description = description  # описание задачи

        self.status = status # статус задачи

        self.assigned_employee: Optional[Employee] = None  # назначенный сотрудник(объект класса Employee)

    # Метод назначает задачу сотруднику
    def assign_employee(self, employee: Employee):
        if not isinstance(employee, Employee):
            raise ValueError("Значение не является объектом класса Employee!")
        else:
            self.assigned_employee = employee
            return employee.emp_id

    # Метод отмечает задачу как завершённую
    def mark_complete(self):
        self.status = TaskStatus.FINISHED.value
        return self.status

    # Метод возвращает задачу в работу
    def mark_in_progress(self):
        self.status = TaskStatus.IN_PROGRESS.value
        return self.status
