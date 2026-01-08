from Task import Task, TaskStatus
from typing import List


class Project:
    # Конструктор класса
    def __init__(self, prj_id, title):
        self.prj_id = prj_id
        if not isinstance(title, str) or not title:
            raise ValueError("Название проекта должно быть непустой строкой!")
        self.title = title #название проекта

        self.tasks: List[Task] = [] #список задач(объекты Task)

    # Метод добавляет задачу к проекту
    def add_task(self, task: Task):
        if not isinstance(task, Task):
            raise ValueError("Задача должна быть объектом класса Task!")
        else:
            self.tasks.append(task)
            return task.task_id

    # Метод возвращает процент завершения проекта на основе статуса задач
    def project_progress(self):
        count_finished = 0

        if len(self.tasks) == 0:
            return f"Проекту не назначены задачи."

        for task in self.tasks:
            if task.status == TaskStatus.FINISHED.value:
                count_finished += 1

        return f"{round(count_finished / len(self.tasks) * 100, 2)} %"