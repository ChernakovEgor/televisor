import sqlite3
from time import sleep
import asyncio

reports = [

    {'id': 'abc', 'name': 'Отчёт за январь', 'pdf_num': 1},
    {'id': 'def', 'name': 'Отчёт за февраль', 'pdf_num': 1},
    {'id': 'ghi', 'name': 'Отчёт за март', 'pdf_num': 1},
    {'id': 'jkl', 'name': 'Отчёт за апрель', 'pdf_num': 1},
]

database = 'dev.db'

def get_report(id: str):
    pass

def get_reports():
    con = sqlite3.connect(database)
    cur = con.cursor()
    res = cur.execute("SELECT * FROM report")
    return res.fetchall()

def update_pdf(id: str, pdf_num: int, pdf: bytes):
    pass

def delete_report(id: str):
    pass

def insert_report(id: str):
    pass

async def fetchall_async(conn, query):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, lambda: conn.cursor().execute(query).fetchall())
