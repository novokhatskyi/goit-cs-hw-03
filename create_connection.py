import psycopg2

def create_connection():
    try:
        conn = psycopg2.connect(
            dbname="task_manager",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        print ("Зєднання з базою успішне")
        return conn
    except Exception as e:
        print ("Error connect:", e)

if __name__ == "__main__":
    conn = create_connection()