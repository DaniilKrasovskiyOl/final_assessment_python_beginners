from Employee import Employee
from Task import Task
from Project import Project
from Table_methods import *
import os

# Создание списка сотрудников - объектов класса Employee
employees = [
    Employee(101,'Дмитрий Краснов', 'Разработчик', 100000.0, 'krasn_dmitr@mail.ru'),
    Employee(102, 'Александр Никитин', 'Разработчик', 110000.0, 'kit_ne_sanya@mail.ru'),
    Employee(103, 'Елена Афанасьева', 'Аналитик', 95000.0, 'elfanas@yandex.ru'),
    Employee(104,'Наталья Высоцкая', 'Аналитик', 89000.0, 'vysotskiy_van_lave@mail.ru'),
    Employee(105,'Артём Казаков', 'Тестировщик', 90000.0, 'kazak_art@yandex.ru'),
    Employee(106,'Ирина Волобуева', 'Тестировщик', 95000.0, 'volobuy_irina@mail.ru')
]

# Создаём csv файл, если его ещё нет для таблицы сотрудников
with open('employees_file.csv', 'w') as f_e:
    create_employees_csv(employees)

# Создание списка задач для проекта Альфа
tasks = [
    Task(10,'Реализация интеграции с внешней системой 1', 'Необходимо реализовать интеграцию с внешней системой 1'),
    Task(11,'Оценить новый бизнес-процесс для работы с системой 1', 'Необходимо оценить новый бизнес-процесс для работы с системой 1'),
    Task(12,'Тестирование интеграции с системой 1', 'Необходимо подготовить автотесты интеграции с системой 1'),
    Task(20,'Реализация интеграции с внешней системой 2', 'Необходимо реализовать интеграцию с внешней системой 2'),
    Task(21,'Оценить новый бизнес-процесс для работы с системой 2', 'Необходимо оценить новый бизнес-процесс для работы с системой 2'),
    Task(22,'Тестирование интеграции с системой 2', 'Необходимо подготовить автотесты интеграции с системой 2'),
    Task(30,'Реализация интеграции с внешней системой 3', 'Необходимо реализовать интеграцию с внешней системой 3'),
    Task(31,'Оценить новый бизнес-процесс для работы с системой 3', 'Необходимо оценить новый бизнес-процесс для работы с системой 3'),
    Task(32,'Тестирование интеграции с системой 3', 'Необходимо подготовить автотесты интеграции с системой 3')
]

# Создаём csv файл, если его ещё нет для таблицы задач
with open('tasks_file.csv', 'w') as f:
    create_tasks_csv(tasks)

# Создание списка проектов
projects = [
    Project(1, 'Проект системы 1'),
    Project(2, 'Проект системы 2'),
    Project(3, 'Проект системы 3')
]

# Создаём csv файл, если его ещё нет для таблицы проектов
with open('projects.csv', 'w') as f_t:
    create_projects_csv(projects)


if __name__ == '__main__':
    """Демонстрационный пример использования всех классов и функций."""
    print("=" * 50)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ СИСТЕМЫ УЧЁТА РАБОЧЕГО ВРЕМЕНИ")
    print("=" * 50)

    print("1. Работа с сотрудниками - Employees:")

    print("\nПри старте программы создаётся файл с начальными данными:")

    df_employees = pd.read_csv('employees_file.csv')

    print(df_employees)

    print("\n1.1. СОЗДАНИЕ СОТРУДНИКОВ:")

    employee_1 = Employee(107,'Яна Васильева', 'Разработчик', 105000.0, 'vasilyan@mail.ru')
    employee_2 = Employee(108, 'Игорь Витальев', 'Аналитик', 100000.0, 'igoryan_vit@yandex.ru')
    employee_3 = Employee(109,'Павел Аристов', 'Тестировщик', 95000.0, 'pal_arist@mail.ru')

    print("\nПосле добавления сотрудников можем посмотреть на обновленную таблицу в файле:")

    df_employees = pd.read_csv('employees_file.csv')

    print(df_employees)

    print("\n1.2. Добавляем отработанные часы:")

    employee_1.add_hours(160)  # Полный месяц
    employee_2.add_hours(145)  # Неполный месяц
    employee_3.add_hours(180)  # Сверхурочные

    print("\nПосле добавления отработанных часов можем посмотреть на обновленную таблицу в файле:")

    df_employees = pd.read_csv('employees_file.csv')

    print(df_employees)

    print(f"Сотруднику {employee_1._name}")
    print(f"Зарплата к выплате: {employee_1.calculate_pay():.2f} руб.")

    print(f"Сотруднику {employee_2._name}")
    print(f"Зарплата к выплате: {employee_2.calculate_pay():.2f} руб.")

    print(f"Сотруднику {employee_3._name}")
    print(f"Зарплата к выплате: {employee_3.calculate_pay():.2f} руб.")

    print(f"У сотрудника {employee_1._name} EMAIL: {employee_1.extract_email()}.")

    print(f"У сотрудника {employee_2._name} EMAIL: {employee_2.extract_email()}.")

    print(f"У сотрудника {employee_3._name} EMAIL: {employee_3.extract_email()}.")

    print("2. Работа с задачами - Tasks:")

    print("\nПри старте программы создаётся файл с начальными данными:")

    df_tasks = pd.read_csv('tasks_file.csv')

    print(df_tasks)

    print("\n2.1. СОЗДАНИЕ ЗАДАЧ:")
    task_1 = Task(40,'Реализация интеграции с внешней системой 4', 'Необходимо реализовать интеграцию с внешней системой 4')
    task_2 = Task(41,'Оценить новый бизнес-процесс для работы с системой 4', 'Необходимо оценить новый бизнес-процесс для работы с системой 4')
    task_3 = Task(42,'Тестирование интеграции с системой 4', 'Необходимо подготовить автотесты интеграции с системой 4')

    print("\nПосле добавления задач можем посмотреть на обновленную таблицу в файле:")

    df_tasks = pd.read_csv('tasks_file.csv')

    print(df_tasks)

    print("\n2.2. НАЗНАЧЕНИЕ ЗАДАЧ СОТРУДНИКАМ:")
    task_1.assign_employee(employee_1)
    task_2.assign_employee(employee_2)
    task_3.assign_employee(employee_3)

    print("\n2.3. Пометим первую и третью задачи как завершённые:")
    task_1.mark_complete()
    task_3.mark_complete()

    print("3. Работа с проектами - Projects:")

    print("\nПри старте программы создаётся файл с начальными данными:")

    df_projects = pd.read_csv('projects_file.csv')

    print(df_projects)
    print("\n3.1. СОЗДАНИЕ ПРОЕКТА:")
    project_1 = Project(4, 'Проект системы 4')

    print("\nПосле добавления проекта можем посмотреть на обновленную таблицу в файле:")

    df_projects = pd.read_csv('projects_file.csv')

    print(df_projects)
    print("\n3.2. ДОБАВИМ ЗАДАЧИ К ПРОЕКТУ:")
    project_1.add_task(task_1)
    project_1.add_task(task_2)
    project_1.add_task(task_3)

    print("\nПосле добавления задач в проект можем посмотреть на обновленную таблицу в файле с задачами (там отмечается проект):")

    print("\n3.3. ПОСМОТРИМ СТЕПЕНЬ ЗАВЕРШЁННОСТИ ПРОЕКТА:")
    print(f"По проекту {project_1._title} процент завершённости составляет: {project_1.project_progress()}.")

    print("\n4. Демонстрация работы функции по удалению строк в csv файле с пропущенными значениями:")

    print("\nДо работы функции:")

    df_tasks = pd.read_csv('tasks_file.csv')

    print(df_tasks)

    read_csv_to_df('tasks_file.csv')

    print("\nПосле работы функции:")

    df_tasks = pd.read_csv('tasks_file.csv')

    print(df_tasks)