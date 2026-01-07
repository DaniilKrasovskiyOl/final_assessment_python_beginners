from Task import Task, TaskStatus
from typing import List
import Table_methods


class Project:
    # Конструктор класса
    def __init__(self, prj_id, title):
        self._prj_id = prj_id
        if not isinstance(title, str) or not title:
            raise ValueError("Название проекта должно быть непустой строкой!")
        self._title = title #название проекта

        self._tasks: List[Task] = [] #список задач(объекты Task)

        Table_methods.create_new_project(self)

    # Метод добавляет задачу к проекту
    def add_task(self, task: Task):
        if not isinstance(task, Task):
            raise ValueError("Задача должна быть объектом класса Task!")
        else:
            self._tasks.append(task)
            Table_methods.update_task_field(task._task_id, 'Project_ID', self._prj_id)

    # Метод возвращает процент завершения проекта на основе статуса задач
    def project_progress(self):
        count_finished = 0
        for task in self._tasks:
            if task.status == TaskStatus.FINISHED.value:
                count_finished += 1

        return f"{round(count_finished / len(self._tasks) * 100, 2)} %"