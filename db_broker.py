import sqlite3
import aiosqlite
import asyncio

def get_select_queries(id: str):
    report_query = 'SELECT 1;'
    pdf_query = 'SELECT 1;'
    section_query = 'SELECT 1;'
    hyperlink_query = 'SELECT 1;'
    return [report_query, pdf_query, section_query, hyperlink_query]

def sleep_query(num):
    query = f"""
    WITH RECURSIVE r(i) AS (
  VALUES(0)
  UNION ALL
  SELECT i FROM r
  LIMIT {num}0000000
  )
  SELECT i FROM r WHERE i = 1;
    """
    return query

async def fetch_async(query, db1):
    async with aiosqlite.connect(database) as db:
        db.row_factory = row_factory
        async with db.execute(query) as cursor:
            res = await cursor.fetchall()
            return res

def fetch(query):
    con = sqlite3.connect(database)
    con.row_factory = row_factory
    res = con.execute(query).fetchall()
    con.close()
    return res

async def get_report(id: str):

        tasks = [asyncio.create_task(fetch_async(query, 1)) for query in get_select_queries(id)]
        done, pending = await asyncio.wait(tasks)
        return [task.result() for task in done]

def get_reports():
    # res = con.execute("SELECT * FROM report").fetchall()
    # res = cur.execute("SELECT * FROM report")
    return fetch("SELECT * FROM report")

def update_pdf(id: str, pdf_num: int, pdf: bytes):
    pass

def update_report(id: str):
    pass

def delete_report(id: str):
    pass

def insert_report(id: str):
    pass

def row_factory(cursor: sqlite3.Cursor, row):
    keys = [result[0] for result in cursor.description]
    return {key: value for key, value in zip(keys, row)}

database = 'dev.db'

# cur = con.cursor()

async def main():   
    print(await get_report('123'))

if __name__ == "__main__":
    asyncio.run(main())
