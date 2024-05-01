import psycopg2
from psycopg2 import extras


def connection():
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        dbname='dilmuss',
        password='sherzodaaa123',
        user='postgres'
    )
    return conn



