from Employee import Employee
from Task import Task
from Project import Project
from Table_methods import *
import pandas as pd
import os
import psycopg2
import tkinter as tk
from tkinter import ttk, messagebox

# ===== Подключение к базе =====

conn = psycopg2.connect(
    host="localhost",
    database="postgres",  # имя вашей базы
    user="postgres",
    password="1234",
    port=5432
)

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


# ===== Функции =====

def refresh_employees_table():
    """Обновляем таблицу, загружая данные из базы"""

    for row in table_employees.get_children():
        table_employees.delete(row)
    cur.execute("SELECT * FROM employees ORDER BY id")
    for row in cur.fetchall():
        table_employees.insert("", "end", values=row)


def refresh_projects_table():
    """Обновляем таблицу, загружая данные из базы"""

    for row in table_projects.get_children():
        table_projects.delete(row)
    cur.execute("SELECT * FROM projects ORDER BY id")
    for row in cur.fetchall():
        table_projects.insert("", "end", values=row)


def refresh_tasks_table():
    """Обновляем таблицу, загружая данные из базы"""

    for row in table_tasks.get_children():
        table_tasks.delete(row)
    cur.execute("SELECT * FROM tasks ORDER BY id")
    for row in cur.fetchall():
        table_tasks.insert("", "end", values=row)


def create_new_employee():
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

    # Проверка уникальности идентификатора
    def check_unique_id():
        value = id_entry.get()  # Получаем значение из поля ввода
        if value:
            # Проверяем, есть ли уже такой ID
            cur.execute("SELECT 1 FROM employees WHERE id=%s", (value,))

            if cur.fetchone() is None:
                # ID не найден, значит всё корректно
                return True
            else:
                # ID уже существует
                return False
        else:
            return False

    # Проверка, что значение зарплаты соответствует типу данных float
    def check_salary_is_float():
        value = salary_entry.get()  # Получаем значение из поля ввода
        try:
            float(value)
            return True
        except ValueError:
            return False

    def insert_new_employee():

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
            new_employee = Employee(employee_id, employee_name, employee_position, float(employee_salary), employee_email)

            cur.execute("INSERT INTO employees (id, name, position, salary, email) VALUES (%s, %s, %s, %s, %s)",
                        (new_employee.emp_id, new_employee.name, new_employee.position, new_employee.salary,
                         new_employee.email))
            conn.commit()
            refresh_employees_table()
            new_window.destroy()  # Закрываем всплывающее окно

    submit_button = tk.Button(new_window, text="OK", command=insert_new_employee)
    submit_button.pack(pady=10)

def add_hours_employee():
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

    # Кнопка для подтверждения
    def get_value():
        value = hours_entry.get()  # Получаем значение из поля ввода
        if value:
            if value.isdigit():
                messagebox.showinfo("Получено", f"Вы ввели: {value}")
                hours = selected_employee.add_hours(int(value))
                row_id = table_employees.item(selected, "values")[0]
                cur.execute("UPDATE employees SET hours_worked = %s WHERE id=%s", (hours, row_id))
                conn.commit()
                refresh_employees_table()
                new_window.destroy()  # Закрываем всплывающее окно
            else:
                messagebox.showwarning("Внимание", "Пожалуйста, введите целое число.")
        else:
            messagebox.showwarning("Внимание", "Пожалуйста, введите значение.")

    submit_button = tk.Button(new_window, text="OK", command=get_value)
    submit_button.pack(pady=10)


def calculate_pay_employee():
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
    cur.execute("SELECT * FROM employees ORDER BY id")
    rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=["ID", "Имя", "Должность", "Зарплата", "EMAIL", "Кол-во отработанных часов"])
    df.to_excel("employees.xlsx", index=False)
    messagebox.showinfo("Успех", "Данные успешно экспортированы в employees.xlsx")


def export_projects_to_excel():
    """Выгрузка данных по проектам в Excel"""
    cur.execute("SELECT * FROM projects ORDER BY id")
    rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=["ID", "Название проекта"])
    df.to_excel("projects.xlsx", index=False)
    messagebox.showinfo("Успех", "Данные успешно экспортированы в projects.xlsx")


def export_tasks_to_excel():
    """Выгрузка данных по задачам в Excel"""
    cur.execute("SELECT * FROM tasks ORDER BY id")
    rows = cur.fetchall()
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

tk.Button(frame_projects, text="Экспорт в Excel", command=export_projects_to_excel).pack(fill="x", padx=10, pady=5)
tk.Button(frame_projects, text="Обновить таблицу проектов", command=refresh_projects_table).pack(fill="x", padx=10,
                                                                                                 pady=5)

# Вкладка задач

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
