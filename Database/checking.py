from psycopg2 import extras

from Database.connection import connection


def is_user_authenticated(user_chat_id):
    conn = connection()
    cursor = conn.cursor(cursor_factory=extras.DictCursor)
    try:
        cursor.execute("SELECT COUNT(*) FROM users WHERE user_chat_id = %s", (user_chat_id,))
        authenticated = cursor.fetchone()[0]
        return authenticated > 0
    finally:
        conn.close()


def insert_user(user_data: dict):
    conn = connection()
    cursor = conn.cursor(cursor_factory=extras.DictCursor)
    try:
        insert_query = """
                    INSERT INTO users (name, branch_id, time, team_id, user_chat_id)
                    VALUES (%s, %s, %s, %s, %s)
                """
        cursor.execute(insert_query, (
            user_data.get('name'),
            user_data.get('branch_id'),
            user_data.get('time'),
            user_data.get('team_id'),
            user_data.get('user_chat_id'),
        ))
        conn.commit()
    except Exception as e:
        print(f'Error inserting user data {e}')
    finally:
        conn.close()


def insert_data_to_base(data: dict):
    conn = connection()
    cursor = conn.cursor(cursor_factory=extras.DictCursor)
    filtered_data = {k: v for k, v in data.items() if v is not None}

    columns = ', '.join(filtered_data.keys())
    values = tuple(filtered_data.values())
    placeholders = ', '.join(['%s'] * len(filtered_data))

    query = f"INSERT INTO user_statistics ({columns}) VALUES ({placeholders})"
    cursor.execute(query, values)
    conn.commit()
    conn.close()
