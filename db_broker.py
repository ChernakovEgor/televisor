import sqlite3
import aiosqlite
import asyncio

def get_select_queries(id: str):
    report_query = f"SELECT id, name FROM report WHERE id = '{id}';"
    pdf_query = f"SELECT num, refresh_interval_ms, path FROM pdf WHERE id_report = '{id}'"
    section_query = f"SELECT name, slides, pdf_num, icon_path FROM section WHERE id_report = '{id}'"
    hyperlink_query = f"SELECT name, slide_num, pdf_num FROM hyperlink WHERE id_report = '{id}'"
    return {'report': report_query, 'pdf': pdf_query, 'section': section_query, 'hyperlink': hyperlink_query}

def get_select_queries_all():
    report_query = f"SELECT id, name FROM report"
    pdf_query = f"SELECT num, refresh_interval_ms, path FROM pdf"
    section_query = f"SELECT name, slides, pdf_num, icon_path FROM section"
    hyperlink_query = f"SELECT name, slide_num, pdf_num FROM hyperlink"
    return {'report': report_query, 'pdf': pdf_query, 'section': section_query, 'hyperlink': hyperlink_query}
   

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

async def fetch_async(table: str, query: str):
    async with aiosqlite.connect(database) as db:
        db.row_factory = row_factory
        async with db.execute(query) as cursor:
            res = await cursor.fetchall()
            return {table: res}

def fetch(query):
    con = sqlite3.connect(database)
    con.row_factory = row_factory
    res = con.execute(query).fetchall()
    con.close()
    return res

async def get_report(id: str):
    tasks = [asyncio.create_task(fetch_async(table, query)) for table, query in get_select_queries(id).items()]
    done, _ = await asyncio.wait(tasks)
    # return [task.result() for task in done]
    res = {}
    for task in done:
        if 'report' in task.result():
            report = list(task.result()['report'])
            res.update(report[0])
        else:
            res.update(task.result())
    return res

async def get_reports():
    tasks = [asyncio.create_task(fetch_async(table, query)) for table, query in get_select_queries_all().items()]
    done, _ = await asyncio.wait(tasks)
    res = {}
    for task in done:
        res.update(task.result())
    # return [task.result() for task in done]
    return res

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
    result1 = (await get_report('1'))
    result = (await get_reports())
    # for row in result1:
    #     print(row)
    #     print()
    print(result1)

if __name__ == "__main__":
    asyncio.run(main())
