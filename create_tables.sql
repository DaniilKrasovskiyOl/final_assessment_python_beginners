DROP TABLE IF EXISTS employees CASCADE;

-- Таблица сотрудников
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    position TEXT,
    salary REAL,
    email TEXT,
    hours_worked INTEGER DEFAULT 0
);

COMMENT ON TABLE employees IS 'Таблица сотрудников';
COMMENT ON COLUMN employees.id IS 'Уникальный идентификатор сотрудника';
COMMENT ON COLUMN employees.name IS 'Имя сотрудника';
COMMENT ON COLUMN employees.position IS 'Должность сотрудника';
COMMENT ON COLUMN employees.salary IS 'Зарплата сотрудника';
COMMENT ON COLUMN employees.email IS 'Электронная почта сотрудника';
COMMENT ON COLUMN employees.hours_worked IS 'Кол-во отработанных часов (по умолчанию 0)';

INSERT INTO employees (id, name, position, salary, email) VALUES
(101,'Дмитрий Краснов', 'Разработчик', 100000.0, 'krasn_dmitr@mail.ru'),
(102, 'Александр Никитин', 'Разработчик', 110000.0, 'kit_ne_sanya@mail.ru'),
(103, 'Елена Афанасьева', 'Аналитик', 95000.0, 'elfanas@yandex.ru'),
(104,'Наталья Высоцкая', 'Аналитик', 89000.0, 'vysotskiy_van_lave@mail.ru'),
(105,'Артём Казаков', 'Тестировщик', 90000.0, 'kazak_art@yandex.ru'),
(106,'Ирина Волобуева', 'Тестировщик', 95000.0, 'volobuy_irina@mail.ru');

DROP TABLE IF EXISTS projects CASCADE;

-- Таблица проектов
CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL
);

COMMENT ON TABLE projects IS 'Таблица проектов';
COMMENT ON COLUMN projects.id IS 'Уникальный идентификатор проекта';
COMMENT ON COLUMN projects.title IS 'Название проекта';

INSERT INTO projects (id, title) VALUES
(1, 'Проект системы 1'),
(2, 'Проект системы 2'),
(3, 'Проект системы 3');

DROP TABLE IF EXISTS tasks CASCADE;

-- Таблица задач
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'В процессе',
    project_id INTEGER,
    assigned_employee_id INTEGER,
    FOREIGN KEY (project_id) REFERENCES projects (id),
    FOREIGN KEY (assigned_employee_id) REFERENCES employees (id)
);

COMMENT ON TABLE tasks IS 'Таблица задач';
COMMENT ON COLUMN tasks.id IS 'Уникальный идентификатор задачи';
COMMENT ON COLUMN tasks.title IS 'Название задачи';
COMMENT ON COLUMN tasks.description IS 'Описание задачи';
COMMENT ON COLUMN tasks.status IS 'Статус задачи';
COMMENT ON COLUMN tasks.project_id IS 'Идентификатор проекта';
COMMENT ON COLUMN tasks.assigned_employee_id IS 'Идентификатор сотрудника, которому назначена задача';

INSERT INTO tasks (id, title, description) VALUES
(10,'Реализация интеграции с внешней системой 1', 'Необходимо реализовать интеграцию с внешней системой 1'),
(11,'Оценить новый бизнес-процесс для работы с системой 1', 'Необходимо оценить новый бизнес-процесс для работы с системой 1'),
(12,'Тестирование интеграции с системой 1', 'Необходимо подготовить автотесты интеграции с системой 1'),
(20,'Реализация интеграции с внешней системой 2', 'Необходимо реализовать интеграцию с внешней системой 2'),
(21,'Оценить новый бизнес-процесс для работы с системой 2', 'Необходимо оценить новый бизнес-процесс для работы с системой 2'),
(22,'Тестирование интеграции с системой 2', 'Необходимо подготовить автотесты интеграции с системой 2'),
(30,'Реализация интеграции с внешней системой 3', 'Необходимо реализовать интеграцию с внешней системой 3'),
(31,'Оценить новый бизнес-процесс для работы с системой 3', 'Необходимо оценить новый бизнес-процесс для работы с системой 3'),
(32,'Тестирование интеграции с системой 3', 'Необходимо подготовить автотесты интеграции с системой 3');