import sqlite3
from time import sleep
import asyncio

reports = [

    {'id': 'abc', 'name': 'Отчёт за январь', 'pdf_num': 1},
    {'id': 'def', 'name': 'Отчёт за февраль', 'pdf_num': 1},
    {'id': 'ghi', 'name': 'Отчёт за март', 'pdf_num': 1},
    {'id': 'jkl', 'name': 'Отчёт за апрель', 'pdf_num': 1},
]

def fetch(query):
    res = cur.execute(query)
    return res.fetchall()

def get_report(id: str):
    pass

def get_reports():
    res = cur.execute("SELECT * FROM report")
    return res.fetchall()

def update_pdf(id: str, pdf_num: int, pdf: bytes):
    pass

def update_report(id: str):
    pass

def delete_report(id: str):
    pass

def insert_report(id: str):
    pass

async def fetchall_async(conn, query):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, lambda: conn.cursor().execute(query).fetchall())

def row_factory(cursor: sqlite3.Cursor, row):
    keys = [result[0] for result in cursor.description]
    return {key: value for key, value in zip(keys, row)}

database = 'dev.db'

con = sqlite3.connect(database)
con.row_factory = row_factory
cur = con.cursor()

def main():   
    print(fetch("SELECT * from report where id_report = '1'"))

if __name__ == "__main__":
    main()
