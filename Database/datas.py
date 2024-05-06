from psycopg2 import extras

from Database.connection import connection


def get_user_datas():
    conn = connection()
    cur = conn.cursor(cursor_factory=extras.DictCursor)
    cur.execute("SELECT * FROM users")
    datas = cur.fetchall()
    result = [{key: val for key, val in row.items()} for row in datas]
    conn.close()
    return result


def get_branch_datas():
    conn = connection()
    cur = conn.cursor(cursor_factory=extras.DictCursor)
    cur.execute("SELECT * FROM branch")
    datas = cur.fetchall()
    result = [{key: val for key, val in row.items()} for row in datas]
    return result


def get_branch_data(branch_name: str):
    conn = connection()
    cur = conn.cursor(cursor_factory=extras.DictCursor)
    cur.execute("SELECT id FROM branch WHERE branch = %s", (branch_name,))
    datas = cur.fetchall()
    result = [{key: val for key, val in row.items()} for row in datas]
    conn.close()
    return result


def get_team_data(branch_id: int):
    conn = connection()
    cur = conn.cursor(cursor_factory=extras.DictCursor)
    cur.execute("SELECT * FROM team WHERE branch_id = %s", (branch_id,))
    datas = cur.fetchall()
    result = [{key: val for key, val in row.items()} for row in datas]
    conn.close()
    return result


def get_team_id(team_name: str):
    conn = connection()
    cur = conn.cursor(cursor_factory=extras.DictCursor)
    cur.execute("SELECT id FROM team WHERE team_name = %s", (team_name,))
    datas = cur.fetchall()
    result = [{key: val for key, val in row.items()} for row in datas]
    conn.close()
    return result


def get_user_time(user_chat_id: int):
    conn = connection()
    cur = conn.cursor(cursor_factory=extras.DictCursor)
    cur.execute("SELECT time FROM users WHERE user_chat_id = %s", (user_chat_id,))
    datas = cur.fetchone()
    if datas:
        result = {key: val for key, val in datas.items()}
    else:
        return "Not Found"
    conn.close()
    time = result['time']
    return time


def get_user_chat_id(user_id: int):
    conn = connection()
    cur = conn.cursor(cursor_factory=extras.DictCursor)
    cur.execute("select user_chat_id from users where id = %s", (user_id,))
    datas = cur.fetchone()
    if datas:
        result = {key: val for key, val in datas.items()}
    else:
        return "Not Found"
    conn.close()
    return result['user_chat_id']


def get_all_user_chat_ids():
    conn = connection()
    cur = conn.cursor(cursor_factory=extras.DictCursor)
    cur.execute('select user_chat_id from users')
    datas = cur.fetchall()
    result = [{key: val for key, val in row.items()} for row in datas]
    conn.close()
    return result


def get_user_name(user_chat_id):
    conn = connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT name FROM users WHERE user_chat_id = %s", (user_chat_id,))
        data = cur.fetchone()
        if data is not None:
            return data[0]
        else:
            return "Unknown User"
    except Exception as e:
        print(f"Error retrieving user name: {e}")
        return "Unknown User"
    finally:
        cur.close()
        conn.close()
