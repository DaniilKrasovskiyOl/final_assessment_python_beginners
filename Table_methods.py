import pandas as pd
import os
import csv



def create_new_employee(employee, filename="employees_file.csv"):
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Добавляем данные из объекта
        writer.writerow(employee.to_csv_row())

def update_employee_field(employee_id, employee_field, field_value, filename="employees_file.csv"):
    # 1. Чтение CSV-файла
    df = pd.read_csv(filename)

    # 2. Определяем фильтр: по идентификатору сотрудника
    condition = df['ID'] == employee_id

    # 3. Заполнение по фильтру выбранного поля по заданному значению
    df.loc[condition, employee_field] = field_value

    # 4. Запись в файл
    df.to_csv(filename, index=False)

def create_tasks_csv(tasks):
    """
    Args:
        tasks (list): Список задач.
    """
    # Преобразование списка объектов в словарь, а затем в DataFrame
    tasks_dict = {
        'ID': [task._task_id for task in tasks],
        'Title': [task._title for task in tasks],
        'Description': [task._description for task in tasks],
        'Status': [task.status for task in tasks],
        'Project_ID': [None for task in tasks],
        'Assign_employee_ID': [None for task in tasks]
    }
    df_tasks = pd.DataFrame(tasks_dict)

    # Запись в CSV с заголовками
    df_tasks.to_csv('tasks_file.csv', index=False, encoding='utf-8')

def create_new_task(task, filename="tasks_file.csv"):
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Добавляем данные из объекта
        writer.writerow(task.to_csv_row())

def update_task_field(task_id, task_field, field_value, filename="tasks_file.csv"):
    # 1. Чтение CSV-файла
    df = pd.read_csv(filename)

    # 2. Определяем фильтр: по идентификатору сотрудника
    condition = df['ID'] == task_id

    # 3. Заполнение по фильтру выбранного поля по заданному значению
    df.loc[condition, task_field] = field_value

    # 4. Запись в файл
    df.to_csv(filename, index=False)

def create_projects_csv(projects):
    """
    Args:
        projects (list): Список проектов.
    """
    # Преобразование списка объектов в словарь, а затем в DataFrame
    projects_dict = {
        'ID': [project._prj_id for project in projects],
        'Title': [project._title for project in projects]
    }
    df_projects = pd.DataFrame(projects_dict)

    # Запись в CSV с заголовками
    df_projects.to_csv('projects_file.csv', index=False, encoding='utf-8')

def create_new_project(project, filename="projects_file.csv"):
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Добавляем данные из объекта
        writer.writerow(project.to_csv_row())

def update_project_field(project_id, project_field, project_value, filename="projects_file.csv"):
    # 1. Чтение CSV-файла
    df = pd.read_csv(filename)

    # 2. Определяем фильтр: по идентификатору сотрудника
    condition = df['ID'] == project_id

    # 3. Заполнение по фильтру выбранного поля по заданному значению
    df.loc[condition, project_field] = project_value

    # 4. Запись в файл
    df.to_csv(filename, index=False)