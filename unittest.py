import unittest
from Employee import Employee
from Task import Task, TaskStatus
from Project import Project


class TestEmployee(unittest.TestCase):
    def setUp(self):
        self.employee = Employee(1, 'Test_name', 'Test_position', 10000.0,
                                 'test@mail.ru')  # создаётся НОВЫЙ сотрудник для каждого теста

    def test_add_hours(self):
        # 0. После добавления 10 часов сотруднику, его рабочие часы становятся больше на 10
        old_hours_worked = self.employee.hours_worked
        self.employee.add_hours(10)
        self.assertEqual(self.employee.hours_worked, old_hours_worked + 10)

    def test_calculate_pay(self):
        # 1.1. Проверка рассчёта зарплаты (кол-во отработанных часов <= 160)
        self.employee.hours_worked = 160
        calculated_pay = self.employee.calculate_pay()
        self.assertEqual(calculated_pay, (self.employee.hours_worked * self.employee.salary) / 160)

    def test_calculate_pay_overtime(self):
        # 1.2. Проверка рассчёта зарплаты (кол-во отработанных часов > 160)
        self.employee.hours_worked = 161
        calculated_pay = self.employee.calculate_pay()
        self.assertEqual(calculated_pay, self.salary + ((self.hours_worked - 160) * self.salary) / 80)

    def test_extract_email_correct(self):
        # 2.1. Проверка получения корректного email
        self.employee.email = 'test@mail.ru'  # Корректный email
        extracted_email = self.employee.extract_email()
        self.assertEqual(self.employee.email, extracted_email)

    def test_extract_email_incorrect(self):
        # 2.2. Проверка получения некорректного email
        self.employee.email = 'test@mail.'  # Некорректный email
        extracted_email = self.employee.extract_email()
        self.assertEqual('EMAIL сотрудника некорректен!', extracted_email)


class TestTask(unittest.TestCase):
    def setUp(self):
        self.task = Task(1, 'Test_title', 'Test_description')  # создаётся НОВАЯ задача для каждого теста

    def test_assign_employee(self):
        # 0. После назначения сотрудника, он числится назначенным у задачи
        employee = Employee(1, 'Test_name', 'Test_position', 10000.0, 'test@mail.ru')
        self.task.assign_employee(employee)
        self.assertEqual(self.task.assigned_employee, employee)

    def test_mark_complete(self):
        # 1. Проверка установки статуса завершения по задаче
        self.task.mark_complete()
        self.assertEqual(TaskStatus.FINISHED.value, self.task.status)

    def test_mark_in_progress(self):
        # 1. Проверка установки статуса завершения по задаче
        self.task.mark_in_progress()
        self.assertEqual(TaskStatus.IN_PROGRESS.value, self.task.status)


class TestProject(unittest.TestCase):
    def setUp(self):
        self.project = Project(1, 'Test_title')  # создаётся НОВЫЙ проект для каждого теста

    def test_add_task(self):
        # 0. После добавления задачи, она является частью задач проекта
        task = Task(1, 'Test_title', 'Test_description')
        list_of_tasks = [task]
        self.project.add_task(task)
        self.assertEqual(list_of_tasks, self.project.tasks)

    def test_project_progress(self):
        # 1.
        first_task = Task(1, 'Test_title', 'Test_description')
        second_task = Task(2, 'Test_title_new', 'Test_description_new')
        first_task_status = first_task.mark_complete()
        self.project.add_task(first_task)
        self.project.add_task(second_task)
        expected_project_progress = f"{round(1 / len(self.project.tasks) * 100, 2)} %"
        obtained_project_progress = self.project.project_progress()
        self.assertEqual(obtained_project_progress, expected_project_progress)


if __name__ == "__main__":
    unittest.main()
