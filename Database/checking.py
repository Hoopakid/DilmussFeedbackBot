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
        cursor.execute("""
            INSERT INTO users (name, branch_id, time, team_id, user_chat_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            user_data['name'],
            user_data['branch_id'],
            user_data['time'],
            user_data['team_id'],
            user_data['user_chat_id']
        ))
        conn.commit()
    except Exception as e:
        print(f'Error inserting user data {e}')
    finally:
        conn.close()
