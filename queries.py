import psycopg2
from rich import print

# --------Отримати всі завдання певного користувача------------
def tasks_of_users_id(user_id):
    connection = psycopg2.connect(
    dbname="task_manager",
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432
)
    cursor = connection.cursor()
    cursor.execute("SELECT title FROM tasks WHERE user_id = %s", (user_id,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results
print("[red bold]--------Отримати всі завдання певного користувача------------[/red bold]")
print(tasks_of_users_id(1))

#----------Вибрати завдання за певним статусом.----------------
def task_by_status(status):
    connection = psycopg2.connect(
    dbname="task_manager",
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432
)
    cursor = connection.cursor()
    cursor.execute("SELECT tasks.title FROM tasks JOIN status ON tasks.status_id = status.id WHERE status.name = %s", (status,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results
print("[red bold]----------Вибрати завдання за певним статусом.----------------[/red bold]")
print(task_by_status("new"))
print(len(task_by_status("new")))

#------------Оновити статус конкретного завдання. 
# Змініть статус конкретного завдання на 'in progress' або інший статус----
def update_status(task_id, new_status):
    connection = psycopg2.connect(
    dbname="task_manager",
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432
    )
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE tasks SET status_id = %s WHERE id = %s",
        (new_status, task_id)
    )
    connection.commit() 
    cursor.close()
    connection.close()

#------------Отримати список користувачів, які не мають жодного завдання.  
# Використайте комбінацію SELECT, WHERE NOT IN і підзапит.---------------------
def list_users_without_task():
    connection = psycopg2.connect(
    dbname="task_manager",
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432
)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * FROM users 
        WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks WHERE user_id IS NOT NULL)
    """)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results
res = list_users_without_task()
print("[red bold]---Отримати список користувачів, які не мають жодного завдання[/red bold]")
print(f"List of usrs withouth tasks: {res}")

#------------Додати користувача.  
# Використайте INSERT для додавання нового користувача.---------------------
def add_new_users(name, email):
    connection = psycopg2.connect(
    dbname="task_manager",
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432
)
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO users (fullname, email)
        VALUES (%s, %s)""",(name, email)
    )
    connection.commit() 
    cursor.close()
    connection.close()


#------------Додати нове завдання для конкретного користувача.  
# Використайте INSERT для додавання нового завдання.---------------------
def add_new_task_for_user(user_id, title, status_id, description):
    connection = psycopg2.connect(
    dbname="task_manager",
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432
)
    cursor = connection.cursor()
    cursor.execute(
        """insert into tasks(user_id, title, status_id, description) 
        values (%s, %s, %s, %s)""", (user_id, title, status_id, description)
    )
    connection.commit() 
    cursor.close()
    connection.close()

    # --------Отримати всі завдання, які ще не завершено.---------
    # --------Виберіть завдання, чий статус не є 'завершено'--------
def tasks_not_complete():
    connection = psycopg2.connect(
    dbname="task_manager",
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432
)
    cursor = connection.cursor()
    cursor.execute(
        """select tasks.title, status.name
        from tasks
        join status on tasks.status_id = status.id
        where status.name != 'completed'"""
    )
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results
res = tasks_not_complete()
print("[red bold]Отримати всі завдання, які ще не завершено[/red bold]")
print(f"List of tasks that are not completed: {res}")
print(f"Кількість не виконаних завдань: {len(res)}")

# --------Видалити конкретне завдання.-------- 
# --------Використайте DELETE для видалення завдання за його id.--------
def del_task_by_id(task_id):
    connection = psycopg2.connect(
    dbname="task_manager",
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432
)
    cursor = connection.cursor()
    cursor.execute(
        """delete from tasks where tasks.id = %s""", (task_id,)
    )
    deleted_rows = cursor.rowcount  # Повертає кількість рядків, які були видалені
    connection.commit()
    cursor.close()
    connection.close()
    
    if deleted_rows == 0:
        print(f"Завдання з id = {task_id} відсутнє або вже було видалено.")
    else:
        print(f"Завдання з id = {task_id} успішно видалено.")
print("[red bold]--------Видалити конкретне завдання.--------[/red bold]")
del_task_by_id(2)

# --------Знайти користувачів з певною електронною поштою--------
# --------Використайте SELECT із умовою LIKE для фільтрації за електронною поштою--------
def find_users_by_email_domain(domain):
    connection = psycopg2.connect(
        dbname="task_manager",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE email LIKE %s",
        ('%' + domain,)
    )
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

users = find_users_by_email_domain('@example.org')
print("[red bold]---Знайти користувачів з певною електронною поштою------[/red bold]")
for user in users:
    print(user)

# --------Оновити ім'я користувача--------
# --------Змініть ім'я користувача за допомогою UPDATE--------
def update_user_name(user_id, new_name):
    connection = psycopg2.connect(
        dbname="task_manager",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE users SET fullname = %s WHERE id = %s",
        (new_name, user_id)
    )
    connection.commit()
    if cursor.rowcount == 0:
        print(f"Користувача з id = {user_id} не знайдено.")
    else:
        print(f"Ім’я користувача з id = {user_id} оновлено на '{new_name}'.")
    cursor.close()
    connection.close()
update_user_name(1, "Toni Blear")

# --------Отримати кількість завдань для кожного статусу--------
# --------Використайте SELECT, COUNT, GROUP BY для групування завдань за статусами--------
import psycopg2

def get_task_counts_by_status():
    connection = psycopg2.connect(
        dbname="task_manager",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )
    cursor = connection.cursor()

    cursor.execute("""
        SELECT status.name, COUNT(tasks.id) AS n_tasks
        FROM status
        JOIN tasks ON tasks.status_id = status.id
        GROUP BY status.name
        ORDER BY n_tasks DESC;
    """)

    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

task_counts = get_task_counts_by_status()
print("[red bold]------Отримати кількість завдань для кожного статусу------[/red bold]")
print("Кількість задач по кожному статусу:")
for status, count in task_counts:
    print(f"{status}: {count}")

# --------Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти--------
# --------Використайте SELECT з умовою LIKE в поєднанні з JOIN, щоб вибрати завдання, призначені користувачам--------
# --------чия електронна пошта містить певний домен (наприклад, '%@example.com')--------
def get_task_domain_of_user():
    connection = psycopg2.connect(
        dbname="task_manager",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )
    cursor = connection.cursor()

    cursor.execute("""
        SELECT tasks.*
        FROM tasks
        JOIN users ON tasks.user_id = users.id
        WHERE users.email LIKE '%@example.org';
        """)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results
tasks = get_task_domain_of_user()
print("[red bold]---Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти----[/red bold]")
print(f"Tasks assigned to users with @example.org domain:\n{tasks}")

# --------Отримати список завдань, що не мають опису--------
# --------Виберіть завдання, у яких відсутній опис--------
def get_tasks_without_description():
    connection = psycopg2.connect(
        dbname="task_manager",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT * FROM tasks
        WHERE description IS NULL;
    """)
    
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

tasks = get_tasks_without_description()
print("[red bold]----Отримати список завдань, що не мають опису----[/red bold]")
print(f"Завдання без опису: {tasks}")

# --------Вибрати користувачів та їхні завдання, які є у статусі 'in progress'--------
# Використайте INNER JOIN для отримання списку користувачів та їхніх завдань із певним статусом--------
def get_tasks_with_status(status):
    connection = psycopg2.connect(
        dbname="task_manager",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )
    cursor = connection.cursor()
    
    cursor.execute("""
        select users.fullname, tasks.title 
        from tasks 
        join status on tasks.status_id = status.id
        join users on tasks.user_id = users.id
        where status.name = %s
    """, (status,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results
res =get_tasks_with_status("in progress")
print("[red bold]--------Вибрати користувачів та їхні завдання, які є у статусі 'in progress'--------[/red bold]")
print(res)

# --------Отримати користувачів та кількість їхніх завдань--------
# --------Використайте LEFT JOIN та GROUP BY для вибору користувачів та підрахунку їхніх завдань--------
import psycopg2

def get_users_with_task_count():
    connection = psycopg2.connect(
        dbname="task_manager",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT users.fullname, COUNT(tasks.id) AS n_tasks
        FROM users
        LEFT JOIN tasks ON users.id = tasks.user_id
        GROUP BY users.fullname
        ORDER BY n_tasks DESC;
    """)
    
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

users_with_tasks = get_users_with_task_count()
print("[red bold]--------Отримати користувачів та кількість їхніх завдань--------[/red bold]")
for fullname, count in users_with_tasks:
    print(f"{fullname}: {count} tasks")