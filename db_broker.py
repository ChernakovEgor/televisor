import sqlite3
from multiprocessing import Pool
import aiosqlite
import asyncio
import assets_manager

pdf_query = """
UPDATE pdf
SET pdf_path = (?)
WHERE pdf_id IN (
    SELECT pdf_id
      FROM pdf_in_report
     WHERE report_id = (?)
);
"""

def get_select_queries(id: str):
    report_query = f"SELECT id, name FROM report WHERE id = (?);"
    # pdf_query = join_query
    pdf_query = "SELECT num, refresh_interval_ms, file_name FROM pdf WHERE report_id = (?)"
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

async def select_async(query: str, table: str = '', params = (), as_dict=True):
    async with aiosqlite.connect(database) as db:
        if as_dict:
            db.row_factory = row_factory
        else:
            db.row_factory = single_param_factory
        async with db.execute(query, params) as cursor:
            res = await cursor.fetchall()
            # return {table: res} if table != '' else res
            return {table: res}

async def alter_async(query: str, params = [], dry_run=False):
    if dry_run:
        print(query)
        return
    async with aiosqlite.connect(database) as db:
        await db.execute("PRAGMA foreign_keys = ON;")
        print(query)
        print(params)
        if isinstance(params, list):
            await db.executemany(query, params)
        else:
            await db.execute(query, params)
        await db.commit()

# TODO: add bytes to response
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


async def get_reports_dumb():
    report_ids = await select_async(table='report', query='SELECT id FROM report')
    reports = []
    for id in report_ids['report']:
        reports.append(await get_report(id['id'])) 
    return reports

# works!
async def update_pdf(id: str, pdf_num: int, pdf: bytes):
    name = assets_manager.generate_name(id, pdf_num)
    pdf_path = assets_manager.save_pdf(name=name, data=pdf)
    await alter_async(f"UPDATE pdf SET file_name = (?) WHERE report_id = (?) AND num = (?)", params=(pdf_path, id, pdf_num))
    pdfs = await select_async("SELECT file_name FROM pdf;", table='pdf', as_dict=False)
    assets_manager.clean_up(pdfs['pdf'])

async def update_report(report):
    id = report['id']
    tasks = []
    for key in report:
        if key == 'name':
            task = asyncio.create_task(alter_async(f"UPDATE report SET name = (?) WHERE id = (?);", (report['name'], id)))
            tasks.append(task)
        if key == 'pdf':
            rows = report['pdf']
            for row in rows:
                columns = []
                values = ()
                if 'num' in row:
                   columns.append('num = (?)') 
                   values += (row['num'], ) 
                if 'refresh_interval_ms' in row:
                   columns.append('refresh_interval_ms = (?)') 
                   values += (row['refresh_interval_ms'], )
                set_string = ','.join(columns)
                pdf_update_query = "UPDATE pdf SET " + set_string + " WHERE report_id = (?);"
                print(pdf_update_query)
                print(values)
                task = asyncio.create_task(alter_async(pdf_update_query, values))
                tasks.append(task)

        if key == 'pdf' or key == 'section' or key == 'section':
            rows = report[key]
            for row in rows:
                values = [f"{column} = '{value}'" for column, value in row.items()]
                # ttask = alter_async(f"UPDATE {key} SET {', '.join(values)} WHERE id_report = '{id}';")
                task = alter_async(f"UPDATE (?) SET (?) WHERE id_report = (?);", (key, ', '.join(values), id))
                tasks.append(asyncio.create_task(task))
    # await asyncio.wait(tasks)

# works!
async def delete_report(id: str):
    results = await select_async("SELECT id FROM report WHERE id = (?);", table="report", params=(id,))
    if len(list(results['report'])) == 0:
        return {f"db_error": "no reports with id = {id}"}
    else:
        await alter_async(f"DELETE FROM report WHERE id = (?);", params=(id,))
        pdfs = await select_async("SELECT file_name FROM pdf;", table='pdf', as_dict=False)
        assets_manager.clean_up(pdfs['pdf'])

# works!
# TODO: Add error handling
async def insert_report(report):
    id = report['id']
    name = report['name']
    pdfs = report['pdf']
    sections = report['section']
    hyperlinks = report['hyperlink']

    tasks = []
    await alter_async(f"INSERT INTO report (id, name) VALUES (?, ?);", params=(id, name))

    pdf_insert_query = "INSERT INTO pdf (report_id, num, refresh_interval_ms, file_name) VALUES (?, ?, ?, ?);"
    pdf_values = [(id, params['num'], params['refresh_interval_ms'], assets_manager.save_pdf(assets_manager.generate_name(id, params['num']), params['pdf'])) for params in pdfs]
    tasks.append(asyncio.create_task(alter_async(pdf_insert_query, pdf_values)))

    section_insert_query = "INSERT INTO section (report_id, name, slides, pdf_num, icon_path) VALUES (?, ?, ?, ?, ?);"
    section_values = [(id, section['name'], section['slides'], section['pdf_num'], section['icon_path']) for section in sections]
    tasks.append(asyncio.create_task(alter_async(section_insert_query, section_values)))

    hyperlink_insert_query = "INSERT INTO hyperlink (report_id, name, slide_num, pdf_num) VALUES (?, ?, ?, ?);"
    hyperlink_values = [(id, hl['name'], hl['slide_num'], hl['pdf_num']) for hl in hyperlinks]
    tasks.append(asyncio.create_task(alter_async(hyperlink_insert_query, hyperlink_values)))

    await asyncio.wait(tasks)

def single_param_factory(cursor: sqlite3.Cursor, row):
    return row[0]

def row_factory(cursor: sqlite3.Cursor, row):
    keys = [result[0] for result in cursor.description]
    return {key: value for key, value in zip(keys, row)}

database = 'dev.db'
item_in = {'id': '12', 'name': 'Report 1', 
        'pdf': [{'num': 10, 'refresh_interval_ms': 3600, 'pdf': b'213'},
                {'num': 1, 'refresh_interval_ms': 3600, 'pdf': b'123'}],
        'hyperlink': [{'name': 'mos.ru', 'slide_num': 1, 'pdf_num': 1}, 
                      {'name': 'mos.ru', 'slide_num': 2, 'pdf_num': 1}], 
        'section': [{'name': 'Weekly', 'slides': '[1, 2, 3]', 'pdf_num': 1, 'icon_path': '/icons/1.svg'}, 
                    {'name': 'Realtime', 'slides': '[1, 2, 3]', 'pdf_num': 1, 'icon_path': '/icons/1.svg'}]}

item_udpate = {'id': '1', 'name': 'Report 1', 
        'pdf': [{'num': 10, 'refresh_interval_ms': 3600},
                {'num': 1}],
        'hyperlink': [{'name': 'mos.ru', 'slide_num': 1, 'pdf_num': 1}, 
                      {'name': 'mos.ru', 'slide_num': 2, 'pdf_num': 1}], 
        'section': [{'name': 'Weekly', 'slides': '[1, 2, 3]', 'pdf_num': 1, 'icon_path': '/icons/1.svg'}, 
                    {'name': 'Realtime', 'slides': '[1, 2, 3]', 'pdf_num': 1, 'icon_path': '/icons/1.svg'}]}


async def main():   
    await update_report(item_udpate)

if __name__ == "__main__":
    asyncio.run(main())
