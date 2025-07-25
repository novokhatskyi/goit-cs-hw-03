import psycopg2
import faker
from random import randint

# ---------- Очистка таблиць ----------
def clear_tables():
    connection = psycopg2.connect(
        dbname="task_manager",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks;")
    cursor.execute("DELETE FROM users;")
    cursor.execute("DELETE FROM status;")

    # Скидання лічильників ID
    cursor.execute("ALTER SEQUENCE tasks_id_seq RESTART WITH 1;")
    cursor.execute("ALTER SEQUENCE users_id_seq RESTART WITH 1;")
    cursor.execute("ALTER SEQUENCE status_id_seq RESTART WITH 1;")

    connection.commit()
    cursor.close()
    connection.close()

# ---------- Додавання статусів ----------
def insert_status(name):
    connection = psycopg2.connect(
        dbname="task_manager",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (name,))
    connection.commit()
    cursor.close()
    connection.close()

# ---------- Розставляння статусів по користувачам----------
def insert_all_statuses():
    names_list = ["new", "in progress", "completed"]
    for name in names_list:
        insert_status(name)

# ---------- Генерація фейкових даних ----------
def generate_fake_data(number_users, number_titles) -> tuple():
    fake_users = []# тут зберігатимемо корисувачів
    fake_titles = []# тут зберігатимемо завдання
    '''Візьмемо 10 користувачів з faker і помістимо їх у потрібну змінну'''
    fake_data = faker.Faker()

    # Створимо набір користувачів у кількості number_users
    for _ in range(number_users):
        fake_users.append((fake_data.name(), fake_data.email()))

    # Створимо набір задач у кількості number_titles
    for _ in range(number_titles):
        titles = fake_data.sentence()
        description = fake_data.text()
        status_id = randint(1, 3)
        user_id = randint(1, number_users)
        fake_titles.append((titles, description, status_id, user_id))
    return fake_users, fake_titles

# ---------- Додавання користувачів ----------
def insert_users (fake_users):
    connection = psycopg2.connect(
        dbname="task_manager",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
)
    cursor = connection.cursor()
    cursor.executemany("INSERT INTO users (fullname, email) VALUES (%s, %s)", fake_users)
    connection.commit()
    cursor.close()
    connection.close()

# ---------- Додавання задач ----------
def insert_tasks (fake_tasks):
    connection = psycopg2.connect(
        dbname="task_manager",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
)
    cursor = connection.cursor()
    cursor.executemany("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)", fake_tasks)
    connection.commit()
    cursor.close()
    connection.close()



# ---------- Виклик ----------
if __name__ == "__main__":
    clear_tables()
    insert_all_statuses()
    users, tasks = generate_fake_data(10, 40)
    insert_users(users)
    insert_tasks(tasks)

