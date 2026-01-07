import enum
from Employee import Employee
from typing import Optional
import Table_methods


class TaskStatus(enum.Enum):
    IN_PROGRESS = "В процессе"
    FINISHED = "Завершено"

class Task:
    # Храним все когда-либо использованные значения 'task_id'
    used_ids = set()
    # Конструктор класса
    def __init__(self, task_id, title, description):
        if task_id in self.used_ids:
            # Если значение уже использовалось, бросаем исключение
            raise ValueError(f"ID {task_id} уже используется. Атрибут ID должен быть уникальными.")
        else:
            # Добавляем новое уникальное ID в множество
            self.used_ids.add(task_id)
            self._task_id = task_id
            if not isinstance(title, str) or not title:
                raise ValueError("Название задачи должно быть непустой строкой!")
            self._title = title #название задачи

            if not isinstance(description, str) or not description:
                raise ValueError("Описание задачи должно быть непустой строкой!")
            self._description = description #описание задачи

            self.status = TaskStatus.IN_PROGRESS.value #начальный статус задачи

            self._assigned_employee: Optional[Employee] = None #назначенный сотрудник(объект класса Employee)

            Table_methods.create_new_task(self)

    # Метод назначает задачу сотруднику
    def assign_employee(self, employee: Employee):
        if not isinstance(employee, Employee):
            raise ValueError("Значение не является объектом класса Employee!")
        else:
            self._assigned_employee = employee
            Table_methods.update_task_field(self._task_id, 'Assign_employee_ID', employee._emp_id)

    # Метод отмечает задачу как завершённую
    def mark_complete(self):
        self.status = TaskStatus.FINISHED.value
        Table_methods.update_task_field(self._task_id, 'Status', self.status)

    # Метод для получения данных в виде списка для записи в CSV
    def to_csv_row(self):
        return [self._task_id, self._title, self._description, self.status]