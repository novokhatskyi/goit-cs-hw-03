import psycopg2

def execute_sql_file(filepath):
    with open(filepath, 'r') as f:
        sql = f.read()

    connection = psycopg2.connect(
        dbname="task_manager",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )

    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    execute_sql_file("tables.sql")