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
root.geometry("1000x800")

# ===== Функции =====

def refresh_table():
    """Обновляем таблицу, загружая данные из базы"""
    for row in table.get_children():
        table.delete(row)
    cur.execute("SELECT * FROM employees ORDER BY id")
    for row in cur.fetchall():
        table.insert("", "end", values=row)

def add_hours():
    selected = table.focus()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите сотрудника, которому добавить часы!")
        return
    # Создаем новое окно верхнего уровня
    new_window = tk.Toplevel(root)
    new_window.title("Добавить отработанные часы")
    new_window.geometry("300x150")

    # Создаем метку
    label = tk.Label(new_window, text="Введите кол-во часов:")
    label.pack(pady=10)

    # Создаем поле ввода (Entry)
    entry_var = tk.StringVar() # Переменная для хранения введенного текста
    hours_entry = tk.Entry(new_window, textvariable=entry_var, width=30)
    hours_entry.pack(pady=5)

    # Кнопка для подтверждения
    def get_value():
        value = entry_var.get() # Получаем значение из поля ввода
        if value:
            new_window.destroy() # Закрываем всплывающее окно
        else:
            messagebox.showwarning("Внимание", "Пожалуйста, введите значение.")

    submit_button = tk.Button(new_window, text="OK", command=get_value)
    submit_button.pack(pady=10)

    hours = int(hours_entry.get())
    row_id = table.item(selected, "values")[0]
    cur.execute("UPDATE employees SET hours_worked = %s WHERE id=%s", (hours, row_id))
    conn.commit()
    refresh_table()

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
    df = pd.DataFrame(rows, columns=["ID", "Название задачи", "Описание задачи", "Статус задачи", "Идентификатор проекта", "Идентификатор сотрудника, которому назначена задача"])
    df.to_excel("tasks.xlsx", index=False)
    messagebox.showinfo("Успех", "Данные успешно экспортированы в tasks.xlsx")

# ===== Кнопки =====

tk.Button(root, text="Добавить отработанные часы сотруднику", command=add_hours).pack(fill="x", padx=10, pady=5)
tk.Button(root, text="Экспорт в Excel сотрудников", command=export_employees_to_excel).pack(fill="x", padx=10, pady=5)
tk.Button(root, text="Экспорт в Excel проектов", command=export_projects_to_excel).pack(fill="x", padx=10, pady=5)
tk.Button(root, text="Экспорт в Excel задач", command=export_tasks_to_excel).pack(fill="x", padx=10, pady=5)
tk.Button(root, text="Показать всю таблицу", command=refresh_table).pack(fill="x", padx=10, pady=5)

# ===== Таблица =====

table = ttk.Treeview(root, columns=("id", "name", "position", "salary", "email", "hours_worked"), show="headings")
table.heading("id", text="ID")
table.heading("name", text="Имя")
table.heading("position", text="Должность")
table.heading("salary", text="Зарплата")
table.heading("email", text="EMAIL")
table.heading("hours_worked", text="Кол-во отработанных часов")
table.pack(fill="both", expand=True, padx=10, pady=10)

if __name__ == '__main__':
    # ===== Загрузка данных при старте =====
    refresh_table()
    # ===== Запуск окна =====
    root.mainloop()