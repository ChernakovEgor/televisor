import sqlite3
from multiprocessing import Pool
import aiosqlite
import asyncio
import assets_manager

def get_select_queries(id: str):
    report_query = f"SELECT id, name FROM report WHERE id = (?);"
    pdf_query = join_query
    section_query = f"SELECT name, slides, pdf_num, icon_path FROM section WHERE report_id = (?);"
    hyperlink_query = f"SELECT name, slide_num, pdf_num FROM hyperlink WHERE report_id = (?);"
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

async def select_async(query: str, table: str = '', params = ()):
    async with aiosqlite.connect(database) as db:
        db.row_factory = row_factory
        async with db.execute(query, params) as cursor:
            res = await cursor.fetchall()
            # return {table: res} if table != '' else res
            return {table: res}

async def alter_async(query: str, params = (), dry_run=False):
    if dry_run:
        print(query)
        return
    async with aiosqlite.connect(database) as db:
        await db.execute("PRAGMA foreign_keys = ON;")
        await db.execute(query, params)
        await db.commit()
        return {}

# works!
async def get_report(id: str):
    tasks = [asyncio.create_task(select_async(table=table, query=query, params=(id,))) for table, query in get_select_queries(id).items()]
    done, _ = await asyncio.wait(tasks)
    res = {}
    for task in done:
        if 'report' in task.result():
            report = list(task.result()['report'])
            # res.update(report[0])
            if len(report) == 0:
                return {}
            res.update(report.pop())
        else:
            res.update(task.result())
    return res

async def get_reports():
    tasks = [asyncio.create_task(select_async(table, query)) for table, query in get_select_queries_all().items()]
    done, _ = await asyncio.wait(tasks)
    return [task.result() for task in done]

# works!
async def get_reports_dumb():
    report_ids = await select_async(table='report', query='SELECT id FROM report')
    reports = []
    for id in report_ids['report']:
        reports.append(await get_report(id['id'])) 
    return reports

async def update_pdf(id: str, pdf_num: int, pdf: bytes):
    pdf_path = '/foo/bar.pdf'
    res = await alter_async(f"UPDATE pdf SET path = (?) WHERE id_report = (?) AND num = (?)", params=(pdf_path, id, pdf_num))

async def update_report(report):
    id = report['id']
    tasks = []
    for key in report:
        if key == 'name':
            tasks.append(asyncio.create_task(alter_async(f"UPDATE report SET name = '{report['name']}' WHERE id = '{id}';")))
            tasks.append(asyncio.create_task(alter_async(f"UPDATE report SET name = (?) WHERE id = (?);", (report['name'], id))))
        if key == 'pdf' or key == 'section' or key == 'section':
            rows = report[key]
            for row in rows:
                values = [f"{column} = '{value}'" for column, value in row.items()]
                tasks.append(asyncio.create_task(alter_async(f"UPDATE {key} SET {', '.join(values)} WHERE id_report = '{id}';")))
    await asyncio.wait(tasks)

# works!
async def delete_report(id: str):
    results = await select_async("SELECT id FROM report WHERE id = (?);", table="report", params=(id,))
    if len(list(results['report'])) == 0:
        return {f"db_error": "no reports with id = {id}"}
    else:
        return await alter_async(f"DELETE FROM report WHERE id = (?);", params=(id,))

async def insert_report(report):
    id = report['id']
    name = report['name']
    pdfs = report['pdf']
    sections = report['section']
    hyperlinks = report['hyperlink']
    
    pdf_values = ','.join([f"('{id}', {pdf['num']}, {pdf['refresh_interval_ms']}, '{assets_manager.save_pdf(assets_manager.generate_name(id, pdf['num']) ,pdf['pdf'])}')" for pdf in pdfs])
    section_values = ','.join([f"('{id}', '{section['name']}', '{section['slides']}', {section['pdf_num']}, '{section['icon_path']}')" for section in sections])
    hyperlink_values = ','.join([f"('{id}', '{hl['name']}', {hl['slide_num']}, {hl['pdf_num']})" for hl in hyperlinks])

    tasks = []
    await alter_async(f"INSERT INTO report (id, name) VALUES ('{id}', '{name}');")
    tasks.append(asyncio.create_task(alter_async(f"INSERT INTO pdf (id_report, num, refresh_interval_ms, path) VALUES {pdf_values};")))
    tasks.append(asyncio.create_task(alter_async(f"INSERT INTO section (id_report, name, slides, pdf_num, icon_path) VALUES {section_values};")))
    tasks.append(asyncio.create_task(alter_async(f"INSERT INTO hyperlink (id_report, name, slide_num, pdf_num) VALUES {hyperlink_values};")))

    await asyncio.wait(tasks)

def row_factory(cursor: sqlite3.Cursor, row):
    keys = [result[0] for result in cursor.description]
    return {key: value for key, value in zip(keys, row)}

database = 'dev.db'
item_in = {'id': '13', 'name': 'Report 1', 
        'pdf': [{'num': 10, 'refresh_interval_ms': 3600, 'pdf': b'213'},
                {'num': 1, 'refresh_interval_ms': 3600, 'pdf': b'123'}],
        'hyperlink': [{'name': 'mos.ru', 'slide_num': 1, 'pdf_num': 1}, 
                      {'name': 'mos.ru', 'slide_num': 2, 'pdf_num': 1}], 
        'section': [{'name': 'Weekly', 'slides': '[1, 2, 3]', 'pdf_num': 1, 'icon_path': '/icons/1.svg'}, 
                    {'name': 'Realtime', 'slides': '[1, 2, 3]', 'pdf_num': 1, 'icon_path': '/icons/1.svg'}]}


join_query = f"""
    SELECT num, refresh_interval_ms, pdf_path 
    FROM pdf_in_report
    LEFT JOIN pdf
    ON pdf_in_report.pdf_id = pdf.pdf_id
    WHERE report_id = (?);
"""

# cur = con.cursor()

async def main():   
    print(await delete_report('2'))

if __name__ == "__main__":
    asyncio.run(main())
