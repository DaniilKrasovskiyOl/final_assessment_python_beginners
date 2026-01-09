from Employee import Employee
from Task import Task
from Project import Project
import pandas as pd
import DB_module
import tkinter as tk
from tkinter import ttk, messagebox

# ===== Подключение к базе =====

# Параметры подключения к БД
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_HOST = "localhost"
DB_PORT = "5432"

conn = DB_module.create_connection(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)

cur = conn.cursor()

# ===== Главное окно =====

root = tk.Tk()
root.title("Учёт рабочего времени")
root.geometry("1280x800")

# ===== Набор вкладок =====

notebook = ttk.Notebook()
notebook.pack(expand=True, fill='both')

frame_employees = ttk.Frame(notebook)
frame_projects = ttk.Frame(notebook)
frame_tasks = ttk.Frame(notebook)

frame_employees.pack(fill='both', expand=True)
frame_projects.pack(fill='both', expand=True)
frame_tasks.pack(fill='both', expand=True)

notebook.add(frame_employees, text="Сотрудники")
notebook.add(frame_projects, text="Проекты")
notebook.add(frame_tasks, text="Задачи")


# ===== Функции для сотрудников =====

def refresh_employees_table():
    """Обновляем таблицу, загружая данные из базы"""

    for row in table_employees.get_children():
        table_employees.delete(row)
    select_query = "SELECT * FROM employees ORDER BY id;"
    cursor = DB_module.fetch_data(conn, select_query)
    for row in cursor.fetchall():
        table_employees.insert("", "end", values=row)


def refresh_projects_table():
    """Обновляем таблицу, загружая данные из базы"""

    for row in table_projects.get_children():
        table_projects.delete(row)
    select_query = "SELECT * FROM projects ORDER BY id;"
    cursor = DB_module.fetch_data(conn, select_query)
    for row in cursor.fetchall():
        table_projects.insert("", "end", values=row)


def refresh_tasks_table():
    """Обновляем таблицу, загружая данные из базы"""

    for row in table_tasks.get_children():
        table_tasks.delete(row)
    select_query = "SELECT * FROM tasks ORDER BY id;"
    cursor = DB_module.fetch_data(conn, select_query)
    for row in cursor.fetchall():
        table_tasks.insert("", "end", values=row)


def create_new_employee():
    """Создание нового сотрудника"""
    # Создаем новое окно верхнего уровня
    new_window = tk.Toplevel(root)
    new_window.title("Добавить нового сотрудника")
    new_window.geometry("500x800")

    ttk.Label(new_window, text="Идентификатор:").pack(pady=5)
    id_entry = ttk.Entry(new_window)
    id_entry.pack(fill="x", padx=10)

    ttk.Label(new_window, text="Имя:").pack(pady=5)
    name_entry = ttk.Entry(new_window)
    name_entry.pack(fill="x", padx=10)

    ttk.Label(new_window, text="Должность:").pack(pady=5)
    position_entry = ttk.Entry(new_window)
    position_entry.pack(fill="x", padx=10)

    ttk.Label(new_window, text="Зарплата:").pack(pady=5)
    salary_entry = ttk.Entry(new_window)
    salary_entry.pack(fill="x", padx=10)

    ttk.Label(new_window, text="EMAIL:").pack(pady=5)
    email_entry = ttk.Entry(new_window)
    email_entry.pack(fill="x", padx=10)

    def check_unique_id():
        """Проверка уникальности идентификатора"""
        value = id_entry.get()  # Получаем значение из поля ввода
        if value:
            # Проверяем, есть ли уже такой ID
            select_query = "SELECT 1 FROM employees WHERE id=%s;"
            select_params = (int(value),)
            cursor = DB_module.fetch_data(conn, select_query, select_params)

            if cursor.fetchone() is None:
                # ID не найден, значит всё корректно
                return True
            else:
                # ID уже существует
                return False
        else:
            return False

    def check_salary_is_float():
        """Проверка, что значение зарплаты соответствует типу данных float"""
        value = salary_entry.get()  # Получаем значение из поля ввода
        try:
            float(value)
            return True
        except ValueError:
            return False

    def insert_new_employee():

        """Добавляет нового сотрудника"""

        employee_id = id_entry.get()
        employee_name = name_entry.get()
        employee_position = position_entry.get()
        employee_salary = salary_entry.get()
        employee_email = email_entry.get()

        if employee_id == '' or employee_name == '' or employee_position == '' or employee_salary == '' or employee_email == '':
            messagebox.showwarning("Внимание", "Пожалуйста, введите все значения.")
        elif not check_unique_id():
            messagebox.showwarning("Внимание", "Пожалуйста, укажите новый идентификатор, повторения недопустимы.")
        elif not employee_id.isdigit():
            messagebox.showwarning("Внимание",
                                   "Идентификатор должен быть целым числом, если начинается с 0, то будет конвертировано в число.")
        elif not check_salary_is_float():
            messagebox.showwarning("Внимание", "Зарплата должна быть числом с плавающей точкой или целым числом.")
        else:
            new_employee = Employee(employee_id, employee_name, employee_position, float(employee_salary),
                                    employee_email)

            insert_query = "INSERT INTO employees (id, name, position, salary, email) VALUES (%s, %s, %s, %s, %s);"
            insert_params = (new_employee.emp_id, new_employee.name, new_employee.position, new_employee.salary,
                             new_employee.email)
            DB_module.execute_query(conn, insert_query, insert_params)
            refresh_employees_table()
            new_window.destroy()  # Закрываем всплывающее окно

    submit_button = tk.Button(new_window, text="OK", command=insert_new_employee)
    submit_button.pack(pady=10)


def change_data_employee():
    """Изменение данных сотрудника"""

    selected = table_employees.focus()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите сотрудника, по которму хотите внести изменения!")
        return
    else:
        selected_employee = Employee(table_employees.item(selected, "values")[0],  # ID
                                     table_employees.item(selected, "values")[1],  # name
                                     table_employees.item(selected, "values")[2],  # position
                                     float(table_employees.item(selected, "values")[3]),  # salary
                                     table_employees.item(selected, "values")[4],  # email
                                     table_employees.item(selected, "values")[5])  # hours_worked

    # Создаем новое окно верхнего уровня

    new_window = tk.Toplevel(root)
    new_window.title("Скорректировать данные сотрудника")
    new_window.geometry("500x800")

    ttk.Label(new_window, text="Имя:").pack(pady=5)
    name_entry = ttk.Entry(new_window)
    name_entry.pack(fill="x", padx=10)

    ttk.Label(new_window, text="Должность:").pack(pady=5)
    position_entry = ttk.Entry(new_window)
    position_entry.pack(fill="x", padx=10)

    ttk.Label(new_window, text="Зарплата:").pack(pady=5)
    salary_entry = ttk.Entry(new_window)
    salary_entry.pack(fill="x", padx=10)

    ttk.Label(new_window, text="EMAIL:").pack(pady=5)
    email_entry = ttk.Entry(new_window)
    email_entry.pack(fill="x", padx=10)

    def check_salary_is_float():
        """Проверка, что значение зарплаты соответствует типу данных float"""
        value = salary_entry.get()  # Получаем значение из поля ввода
        try:
            float(value)
            return True
        except ValueError:
            return False

    def update_employee():
        """Обновить информацию по сотруднику"""
        employee_name = name_entry.get()
        employee_position = position_entry.get()
        employee_salary = salary_entry.get()
        employee_email = email_entry.get()

        if not check_salary_is_float:
            messagebox.showwarning("Внимание", "Зарплата должна быть числом с плавающей точкой или целым числом.")
        elif employee_name == '' and employee_position == '' and employee_salary == '' and employee_email == '':
            refresh_employees_table()
            new_window.destroy()  # Закрываем всплывающее окно
        else:
            selected_employee.name = employee_name or selected_employee.name
            selected_employee.position = employee_position or selected_employee.position
            selected_employee.salary = employee_salary or selected_employee.salary
            selected_employee.email = employee_email or selected_employee.email
            update_query = "UPDATE employees SET name = %s, position = %s, salary = %s, email = %s WHERE id=%s;"
            update_params = (selected_employee.name, selected_employee.position, selected_employee.salary,
                             selected_employee.email, selected_employee.emp_id)
            DB_module.execute_query(conn, update_query, update_params)
            refresh_employees_table()
            new_window.destroy()  # Закрываем всплывающее окно

    submit_button = tk.Button(new_window, text="OK", command=update_employee)
    submit_button.pack(pady=10)


def add_hours_employee():
    """Добавить сотруднику отработанные часы"""
    selected = table_employees.focus()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите сотрудника, которому добавить часы!")
        return
    else:
        selected_employee = Employee(table_employees.item(selected, "values")[0],  # ID
                                     table_employees.item(selected, "values")[1],  # name
                                     table_employees.item(selected, "values")[2],  # position
                                     float(table_employees.item(selected, "values")[3]),  # salary
                                     table_employees.item(selected, "values")[4],  # email
                                     table_employees.item(selected, "values")[5])  # hours_worked

    # Создаем новое окно верхнего уровня
    new_window = tk.Toplevel(root)
    new_window.title("Добавить отработанные часы")
    new_window.geometry("300x150")

    ttk.Label(new_window, text="Кол-во часов:").pack(pady=5)
    hours_entry = ttk.Entry(new_window)
    hours_entry.pack(fill="x", padx=10)

    def get_value():
        """Обновление значения отработанных часов"""
        value = hours_entry.get()  # Получаем значение из поля ввода
        if value:
            if value.isdigit():
                messagebox.showinfo("Получено", f"Вы ввели: {value}")
                hours = selected_employee.add_hours(int(value))
                row_id = table_employees.item(selected, "values")[0]
                update_query = "UPDATE employees SET hours_worked = %s WHERE id=%s;"
                update_params = (hours, row_id)
                DB_module.execute_query(conn, update_query, update_params)
                refresh_employees_table()
                new_window.destroy()  # Закрываем всплывающее окно
            else:
                messagebox.showwarning("Внимание", "Пожалуйста, введите целое число.")
        else:
            messagebox.showwarning("Внимание", "Пожалуйста, введите значение.")

    submit_button = tk.Button(new_window, text="OK", command=get_value)
    submit_button.pack(pady=10)


def calculate_pay_employee():
    """Посчитать зарплату сотрудника"""
    selected = table_employees.focus()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите сотрудника, по которому необходимо посчитать зарплату!")
        return
    else:
        selected_employee = Employee(table_employees.item(selected, "values")[0],  # ID
                                     table_employees.item(selected, "values")[1],  # name
                                     table_employees.item(selected, "values")[2],  # position
                                     float(table_employees.item(selected, "values")[3]),  # salary
                                     table_employees.item(selected, "values")[4],  # email
                                     table_employees.item(selected, "values")[5])  # hours_worked

        pay_for_employee = selected_employee.calculate_pay()

        messagebox.showinfo("Получено", f"Сотрудник {selected_employee.name} должен получить: {pay_for_employee}")


def extract_email_employee():
    """Получить EMAIL выбранного сотрудника"""
    selected = table_employees.focus()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите сотрудника, по которому необходимо посчитать зарплату!")
        return
    else:
        selected_employee = Employee(table_employees.item(selected, "values")[0],  # ID
                                     table_employees.item(selected, "values")[1],  # name
                                     table_employees.item(selected, "values")[2],  # position
                                     float(table_employees.item(selected, "values")[3]),  # salary
                                     table_employees.item(selected, "values")[4],  # email
                                     table_employees.item(selected, "values")[5])  # hours_worked

        employee_email = selected_employee.extract_email()

        messagebox.showinfo("Получено", f"У сотрудника {selected_employee.name} email: {employee_email}")


def export_employees_to_excel():
    """Выгрузка данных по сотрудникам в Excel"""
    select_query = "SELECT * FROM employees ORDER BY id;"
    cursor = DB_module.fetch_data(conn, select_query)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["ID", "Имя", "Должность", "Зарплата", "EMAIL", "Кол-во отработанных часов"])
    df.to_excel("employees.xlsx", index=False)
    messagebox.showinfo("Успех", "Данные успешно экспортированы в employees.xlsx")


# ===== Функции для проектов =====

def create_new_project():
    """Создание новго проекта"""

    # Создаем новое окно верхнего уровня
    new_window = tk.Toplevel(root)
    new_window.title("Добавить новый проект")
    new_window.geometry("500x400")

    ttk.Label(new_window, text="Идентификатор:").pack(pady=5)
    id_entry = ttk.Entry(new_window)
    id_entry.pack(fill="x", padx=10)

    ttk.Label(new_window, text="Название проекта:").pack(pady=5)
    title_entry = ttk.Entry(new_window)
    title_entry.pack(fill="x", padx=10)

    def check_unique_id():
        """Проверка уникальности идентификатора"""
        value = id_entry.get()  # Получаем значение из поля ввода
        if value:
            # Проверяем, есть ли уже такой ID
            select_query = "SELECT 1 FROM projects WHERE id=%s;"
            select_params = (int(value),)
            cursor = DB_module.fetch_data(conn, select_query, select_params)

            if cursor.fetchone() is None:
                # ID не найден, значит всё корректно
                return True
            else:
                # ID уже существует
                return False
        else:
            return False

    def insert_new_project():

        """Добавляет новый проект"""

        project_id = id_entry.get()
        project_title = title_entry.get()

        if project_id == '' or project_title == '':
            messagebox.showwarning("Внимание", "Пожалуйста, введите все значения.")
        elif not check_unique_id():
            messagebox.showwarning("Внимание", "Пожалуйста, укажите новый идентификатор, повторения недопустимы.")
        elif not project_id.isdigit():
            messagebox.showwarning("Внимание",
                                   "Идентификатор должен быть целым числом, если начинается с 0, то будет конвертировано в число.")
        else:
            new_project = Project(project_id, project_title)

            insert_query = "INSERT INTO projects (id, title) VALUES (%s, %s);"
            insert_params = (new_project.prj_id, new_project.title)
            DB_module.execute_query(conn, insert_query, insert_params)
            refresh_projects_table()
            new_window.destroy()  # Закрываем всплывающее окно

    submit_button = tk.Button(new_window, text="OK", command=insert_new_project)
    submit_button.pack(pady=10)


def change_project_title():
    """Изменить название проекта"""
    selected = table_projects.focus()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите проект, название которого хотите изменить!")
        return
    else:
        selected_project = Project(table_projects.item(selected, "values")[0],  # ID
                                   table_projects.item(selected, "values")[1])  # title

    # Создаем новое окно верхнего уровня
    new_window = tk.Toplevel(root)
    new_window.title("Изменение названия проекта")
    new_window.geometry("300x150")

    ttk.Label(new_window, text="Введите новое название:").pack(pady=5)
    title_entry = ttk.Entry(new_window)
    title_entry.pack(fill="x", padx=10)

    def get_value():
        """Обновление наименования проекта"""
        value = title_entry.get()  # Получаем значение из поля ввода
        if value:
            selected_project.title = value
            update_query = "UPDATE projects SET title = %s WHERE id=%s;"
            update_params = (selected_project.title, selected_project.prj_id)
            DB_module.execute_query(conn, update_query, update_params)
            refresh_projects_table()
            new_window.destroy()
        else:
            messagebox.showwarning("Внимание", "Пожалуйста, введите значение.")

    submit_button = tk.Button(new_window, text="OK", command=get_value)
    submit_button.pack(pady=10)


def add_task_to_project():
    """Добавить к проекту задачу"""
    selected = table_projects.focus()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите проект, для которого хотели добавить задачу!")
        return
    else:
        selected_project = Project(table_projects.item(selected, "values")[0],  # ID
                                   table_projects.item(selected, "values")[1])  # title

    # Создаем новое окно верхнего уровня
    new_window = tk.Toplevel(root)
    new_window.title("Добавление задачи к проекту")
    new_window.geometry("300x150")

    ttk.Label(new_window, text="Введите идентификатор задачи:").pack(pady=5)
    task_id_entry = ttk.Entry(new_window)
    task_id_entry.pack(fill="x", padx=10)

    def check_exist_task_id():
        """Проверка существования введённого идентификатора задачи"""
        value = task_id_entry.get()  # Получаем значение из поля ввода
        if value:
            # Проверяем, есть ли уже такой ID
            select_query = "SELECT 1 FROM tasks WHERE id=%s;"
            select_params = (int(value),)
            cursor = DB_module.fetch_data(conn, select_query, select_params)

            if cursor.fetchone() is None:
                # ID не найден
                return False
            else:
                # ID существует
                return True
        else:
            return False

    def add_project_id_to_task():

        """Добавляет проект к задаче"""

        task_id = task_id_entry.get()

        if not task_id.isdigit():
            messagebox.showwarning("Внимание",
                                   "Идентификатор должен быть целым числом, если начинается с 0, то будет конвертировано в число.")
        elif not check_exist_task_id():
            messagebox.showwarning("Внимание", "Пожалуйста, укажите существующий идентификатор задачи.")
        else:
            update_query = "UPDATE tasks SET project_id = %s WHERE id = %s;"
            update_params = (selected_project.prj_id, int(task_id))
            DB_module.execute_query(conn, update_query, update_params)
            refresh_tasks_table()
            new_window.destroy()  # Закрываем всплывающее окно

    submit_button = tk.Button(new_window, text="OK", command=add_project_id_to_task)
    submit_button.pack(pady=10)


def get_project_progress():
    """Получение прогресса по выбранной задаче"""
    selected = table_projects.focus()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите проект, для которого хотели бы узнать процент завершённости!")
        return
    else:
        selected_project = Project(table_projects.item(selected, "values")[0],  # ID
                                   table_projects.item(selected, "values")[1])  # title

    select_query = "SELECT id, title, description, status FROM tasks WHERE project_id = %s ORDER BY id;"
    select_params = (selected_project.prj_id,)
    cursor = DB_module.fetch_data(conn, select_query, select_params)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows,
                      columns=["task_id", "title", "description", "status"])
    tasks_objects_list = [Task(*row) for row in df.itertuples(index=False)]
    selected_project.tasks = tasks_objects_list
    selected_project_progress = selected_project.project_progress()
    if len(tasks_objects_list) == 0:
        messagebox.showinfo("Результат", f"{selected_project_progress}")
    else:
        messagebox.showinfo("Результат", f"{selected_project.title} завершён на {selected_project_progress}")


def export_projects_to_excel():
    """Выгрузка данных по проектам в Excel"""
    select_query = "SELECT * FROM projects ORDER BY id;"
    cursor = DB_module.fetch_data(conn, select_query)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["ID", "Название проекта"])
    df.to_excel("projects.xlsx", index=False)
    messagebox.showinfo("Успех", "Данные успешно экспортированы в projects.xlsx")


# ===== Функции для задач =====

def create_new_task():
    """Создание новой задачи"""

    # Создаем новое окно верхнего уровня
    new_window = tk.Toplevel(root)
    new_window.title("Добавить новую задачу")
    new_window.geometry("500x800")

    ttk.Label(new_window, text="Идентификатор:").pack(pady=5)
    id_entry = ttk.Entry(new_window)
    id_entry.pack(fill="x", padx=10)

    ttk.Label(new_window, text="Название:").pack(pady=5)
    title_entry = ttk.Entry(new_window)
    title_entry.pack(fill="x", padx=10)

    ttk.Label(new_window, text="Описание:").pack(pady=5)
    description_entry = ttk.Entry(new_window)
    description_entry.pack(fill="x", padx=10)

    def check_unique_id():
        """Проверка уникальности идентификатора"""
        value = id_entry.get()  # Получаем значение из поля ввода
        if value:
            # Проверяем, есть ли уже такой ID
            select_query = "SELECT 1 FROM tasks WHERE id=%s;"
            select_params = (int(value),)
            cursor = DB_module.fetch_data(conn, select_query, select_params)

            if cursor.fetchone() is None:
                # ID не найден, значит всё корректно
                return True
            else:
                # ID уже существует
                return False
        else:
            return False

    def insert_new_task():

        """Добавляет новую задачу"""

        task_id = id_entry.get()
        task_title = title_entry.get()
        task_description = description_entry.get()

        if task_id == '' or task_title == '' or task_description == '':
            messagebox.showwarning("Внимание", "Пожалуйста, введите все значения.")
        elif not check_unique_id():
            messagebox.showwarning("Внимание", "Пожалуйста, укажите новый идентификатор, повторения недопустимы.")
        elif not task_id.isdigit():
            messagebox.showwarning("Внимание",
                                   "Идентификатор должен быть целым числом, если начинается с 0, то будет конвертировано в число.")
        else:
            new_task = Task(task_id, task_title, task_description)

            insert_query = "INSERT INTO tasks (id, title, description) VALUES (%s, %s, %s);"
            insert_params = (new_task.task_id, new_task.title, new_task.description)
            DB_module.execute_query(conn, insert_query, insert_params)
            refresh_tasks_table()
            new_window.destroy()  # Закрываем всплывающее окно

    submit_button = tk.Button(new_window, text="OK", command=insert_new_task)
    submit_button.pack(pady=10)


def change_data_task():
    """Изменение данных задачи"""

    selected = table_tasks.focus()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите задачу, по которой хотите внести изменения!")
        return
    else:
        selected_task = Task(table_tasks.item(selected, "values")[0],  # ID
                             table_tasks.item(selected, "values")[1],  # title
                             table_tasks.item(selected, "values")[2])  # description

    # Создаем новое окно верхнего уровня

    new_window = tk.Toplevel(root)
    new_window.title("Скорректировать данные задачи")
    new_window.geometry("500x400")

    ttk.Label(new_window, text="Название:").pack(pady=5)
    title_entry = ttk.Entry(new_window)
    title_entry.pack(fill="x", padx=10)

    ttk.Label(new_window, text="Описание:").pack(pady=5)
    description_entry = ttk.Entry(new_window)
    description_entry.pack(fill="x", padx=10)

    def update_task():
        """Обновить информацию по задаче"""
        task_title = title_entry.get()
        task_description = description_entry.get()

        if task_title == '' and task_description == '':
            refresh_employees_table()
            new_window.destroy()  # Закрываем всплывающее окно
        else:
            selected_task.title = task_title or selected_task.title
            selected_task.description = task_description or selected_task.description
            update_query = "UPDATE tasks SET title = %s, description = %s WHERE id=%s;"
            update_params = (selected_task.title, selected_task.description, selected_task.task_id)
            DB_module.execute_query(conn, update_query, update_params)
            refresh_tasks_table()
            new_window.destroy()  # Закрываем всплывающее окно

    submit_button = tk.Button(new_window, text="OK", command=update_task)
    submit_button.pack(pady=10)


def assign_task_to_employee():
    """Назначить задачу сотруднику"""
    selected = table_tasks.focus()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите задачу, которую хотите назначить сотруднику!")
        return
    else:
        selected_task = Task(table_tasks.item(selected, "values")[0],  # ID
                             table_tasks.item(selected, "values")[1],  # title
                             table_tasks.item(selected, "values")[2],  # description
                             table_tasks.item(selected, "values")[3])  # status

    # Создаем новое окно верхнего уровня
    new_window = tk.Toplevel(root)
    new_window.title("Назначение задачи сотруднику")
    new_window.geometry("300x150")

    ttk.Label(new_window, text="Введите идентификатор сотрудника:").pack(pady=5)
    emp_id_entry = ttk.Entry(new_window)
    emp_id_entry.pack(fill="x", padx=10)

    def check_exist_emp_id():
        """Проверка существования введённого идентификатора сотрудника"""
        value = emp_id_entry.get()  # Получаем значение из поля ввода
        if value:
            # Проверяем, есть ли уже такой ID
            select_query = "SELECT 1 FROM employees WHERE id=%s;"
            select_params = (int(value),)
            cursor = DB_module.fetch_data(conn, select_query, select_params)

            if cursor.fetchone() is None:
                # ID не найден
                return False
            else:
                # ID существует
                return True
        else:
            return False

    def add_emp_id_to_task():

        """Добавляет сотрудника к задаче"""

        emp_id = emp_id_entry.get()

        if not emp_id.isdigit():
            messagebox.showwarning("Внимание",
                                   "Идентификатор должен быть целым числом, если начинается с 0, то будет конвертировано в число.")
        elif not check_exist_emp_id():
            messagebox.showwarning("Внимание", "Пожалуйста, укажите существующий идентификатор сотрудника.")
        else:
            select_query = "SELECT * FROM employees WHERE id=%s;"
            select_params = (int(emp_id),)
            cursor = DB_module.fetch_data(conn, select_query, select_params)
            row = cursor.fetchone()
            assigned_employee = Employee(row[0], row[1], row[2], row[3], row[4], row[5])
            assigned_employee_id = selected_task.assign_employee(assigned_employee)
            messagebox.showinfo("Результат",
                                f"Задача {selected_task.title} назначена сотруднику {assigned_employee.name}!")
            update_query = "UPDATE tasks SET assigned_employee_id = %s WHERE id = %s;"
            update_params = (assigned_employee_id, selected_task.task_id)
            DB_module.execute_query(conn, update_query, update_params)
            refresh_tasks_table()
            new_window.destroy()  # Закрываем всплывающее окно

    submit_button = tk.Button(new_window, text="OK", command=add_emp_id_to_task)
    submit_button.pack(pady=10)


def mark_task_complete():
    """Пометить задачу как завершённую"""
    selected = table_tasks.focus()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите задачу, которую хотите завершить!")
        return
    else:
        selected_task = Task(table_tasks.item(selected, "values")[0],  # ID
                             table_tasks.item(selected, "values")[1],  # title
                             table_tasks.item(selected, "values")[2])  # description

        task_status = selected_task.mark_complete()

        messagebox.showinfo("Результат", f"Задача {selected_task.title} теперь имеет статус: {task_status}!")

        update_query = "UPDATE tasks SET status = %s WHERE id = %s;"
        update_params = (task_status, selected_task.task_id)
        DB_module.execute_query(conn, update_query, update_params)
        refresh_tasks_table()


def mark_task_in_progress():
    """Вернуть задачу в работу"""
    selected = table_tasks.focus()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите задачу, которую хотите вернуть в работу!")
        return
    else:
        selected_task = Task(table_tasks.item(selected, "values")[0],  # ID
                             table_tasks.item(selected, "values")[1],  # title
                             table_tasks.item(selected, "values")[2])  # description

        task_status = selected_task.mark_in_progress()

        messagebox.showinfo("Результат", f"Задача {selected_task.title} теперь имеет статус: {task_status}!")

        update_query = "UPDATE tasks SET status = %s WHERE id = %s;"
        update_params = (task_status, selected_task.task_id)
        DB_module.execute_query(conn, update_query, update_params)
        refresh_tasks_table()


def export_tasks_to_excel():
    """Выгрузка данных по задачам в Excel"""
    select_query = "SELECT * FROM tasks ORDER BY id;"
    cursor = DB_module.fetch_data(conn, select_query)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows,
                      columns=["ID", "Название задачи", "Описание задачи", "Статус задачи", "Идентификатор проекта",
                               "Идентификатор сотрудника, которому назначена задача"])
    df.to_excel("tasks.xlsx", index=False)
    messagebox.showinfo("Успех", "Данные успешно экспортированы в tasks.xlsx")


# ===== Кнопки =====

# Вкладка сотрудников

tk.Button(frame_employees, text="Добавить нового сотрудника", command=create_new_employee).pack(fill="x",
                                                                                                padx=10,
                                                                                                pady=5)
tk.Button(frame_employees, text="Изменить данные сотрудника", command=change_data_employee).pack(fill="x",
                                                                                                 padx=10,
                                                                                                 pady=5)
tk.Button(frame_employees, text="Добавить отработанные часы сотруднику", command=add_hours_employee).pack(fill="x",
                                                                                                          padx=10,
                                                                                                          pady=5)
tk.Button(frame_employees, text="Посчитать зарплату выбранному сотруднику", command=calculate_pay_employee).pack(
    fill="x",
    padx=10, pady=5)
tk.Button(frame_employees, text="Получить email выбранного сотрудника", command=extract_email_employee).pack(fill="x",
                                                                                                             padx=10,
                                                                                                             pady=5)
tk.Button(frame_employees, text="Экспорт в Excel", command=export_employees_to_excel).pack(fill="x", padx=10, pady=5)
tk.Button(frame_employees, text="Обновить таблицу сотрудников", command=refresh_employees_table).pack(fill="x", padx=10,
                                                                                                      pady=5)

# Вкладка проектов
tk.Button(frame_projects, text="Добавить новый проект", command=create_new_project).pack(fill="x",
                                                                                         padx=10,
                                                                                         pady=5)
tk.Button(frame_projects, text="Изменить название проекта", command=change_project_title).pack(fill="x",
                                                                                               padx=10,
                                                                                               pady=5)
tk.Button(frame_projects, text="Назначить проекту задачу", command=add_task_to_project).pack(fill="x",
                                                                                             padx=10,
                                                                                             pady=5)
tk.Button(frame_projects, text="Вывести прогресс проекта", command=get_project_progress).pack(fill="x",
                                                                                              padx=10,
                                                                                              pady=5)
tk.Button(frame_projects, text="Экспорт в Excel", command=export_projects_to_excel).pack(fill="x", padx=10, pady=5)
tk.Button(frame_projects, text="Обновить таблицу проектов", command=refresh_projects_table).pack(fill="x", padx=10,
                                                                                                 pady=5)

# Вкладка задач

tk.Button(frame_tasks, text="Добавить новую задачу", command=create_new_task).pack(fill="x",
                                                                                   padx=10,
                                                                                   pady=5)
tk.Button(frame_tasks, text="Изменить данные по задаче", command=change_data_task).pack(fill="x",
                                                                                        padx=10,
                                                                                        pady=5)

tk.Button(frame_tasks, text="Назначить задачу сотруднику", command=assign_task_to_employee).pack(fill="x",
                                                                                                 padx=10,
                                                                                                 pady=5)
tk.Button(frame_tasks, text="Завершить задачу", command=mark_task_complete).pack(fill="x",
                                                                                 padx=10,
                                                                                 pady=5)
tk.Button(frame_tasks, text="Вернуть задачу в работу", command=mark_task_in_progress).pack(fill="x",
                                                                                           padx=10,
                                                                                           pady=5)
tk.Button(frame_tasks, text="Экспорт в Excel", command=export_tasks_to_excel).pack(fill="x", padx=10, pady=5)
tk.Button(frame_tasks, text="Обновить таблицу задач", command=refresh_tasks_table).pack(fill="x", padx=10, pady=5)

# ===== Таблицы =====

# Таблица сотрудников

table_employees = ttk.Treeview(frame_employees, columns=("id", "name", "position", "salary", "email", "hours_worked"),
                               show="headings")
table_employees.heading("id", text="ID")
table_employees.heading("name", text="Имя")
table_employees.heading("position", text="Должность")
table_employees.heading("salary", text="Зарплата")
table_employees.heading("email", text="EMAIL")
table_employees.heading("hours_worked", text="Кол-во отработанных часов")
table_employees.pack(fill="both", expand=True, padx=10, pady=10)

# Таблица проектов

table_projects = ttk.Treeview(frame_projects, columns=("id", "title"), show="headings")
table_projects.heading("id", text="ID")
table_projects.heading("title", text="Название проекта")
table_projects.pack(fill="both", expand=True, padx=10, pady=10)

# Таблица задач

table_tasks = ttk.Treeview(frame_tasks,
                           columns=("id", "title", "description", "status", "project_id", "assigned_employee_id"),
                           show="headings")
table_tasks.heading("id", text="ID")
table_tasks.heading("title", text="Название задачи")
table_tasks.heading("description", text="Описание задачи")
table_tasks.heading("status", text="Статус задачи")
table_tasks.heading("project_id", text="Идентификатор проекта")
table_tasks.heading("assigned_employee_id", text="Идентификатор сотрудника, которому назначена задача")
table_tasks.pack(fill="both", expand=True, padx=10, pady=10)

if __name__ == '__main__':
    # ===== Загрузка данных при старте =====
    refresh_employees_table()
    refresh_projects_table()
    refresh_tasks_table()
    # ===== Запуск окна =====
    root.mainloop()
