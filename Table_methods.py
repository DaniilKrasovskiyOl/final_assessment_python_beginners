import pandas as pd
import os
import csv


def read_csv_to_df(file_path):
    """
    Читает CSV файл, удаляет строки с любыми пропущенными значениями (NaN, None)
    и сохраняет результат в новый CSV файл.

    Args:
        file_path (str): Путь к исходному CSV файлу.
    """
    try:
        # 1. Чтение CSV файла в DataFrame
        # Используем 'sep=None' и 'engine='python'' для автоматического определения разделителя
        # 'skipinitialspace=True' помогает при лишних пробелах после разделителя
        df = pd.read_csv(file_path, sep=None, engine='python', skipinitialspace=True)  # или 'latin1', 'cp1251'

        # 2. Удаление строк, содержащих хотя бы одно пропущенное значение
        # how='any' - удаляет, если есть хотя бы одно пропущенное значение в строке
        df_cleaned = df.dropna(how='any')

        # 3. Удаление исходного файла
        os.remove(file_path)

        # 4. Сохранение очищенного DataFrame в новый CSV файл
        df_cleaned.to_csv(file_path, index=False)  # index=False, чтобы не записывать индекс DataFrame

    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути {file_path}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def create_employees_csv(employees):
    """
    Args:
        employees (list): Список сотрудников.
    """
    # Преобразование списка объектов в словарь, а затем в DataFrame
    employees_dict = {
        'ID': [employee._emp_id for employee in employees],
        'Name': [employee._name for employee in employees],
        'Position': [employee._position for employee in employees],
        'Salary': [employee._salary for employee in employees],
        'Email': [employee._email for employee in employees],
        'Hours_worked': [employee._hours_worked for employee in employees]
    }
    df_employees = pd.DataFrame(employees_dict)

    # Запись в CSV с заголовками
    df_employees.to_csv('employees_file.csv', index=False, encoding='utf-8')

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