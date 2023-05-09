import sqlite3
import os

database = 'dev.db'

c1 = """CREATE TABLE report (
  id VARCHAR(8) PRIMARY KEY,
  name VARCHAR(255),
  modified DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

t1 = """CREATE TRIGGER report_timestamp AFTER UPDATE ON report
    BEGIN
      UPDATE report
         SET modified = CURRENT_TIMESTAMP
       WHERE id = old.id;
    END;

"""

c2 = """CREATE TABLE pdf (
  report_id VARCHAR(8),
  pdf_id INTEGER PRIMARY KEY,
  refresh_interval_ms int,
  num int8,
  file_name TEXT,
  modified datetime default current_timestamp,
  FOREIGN KEY(report_id) REFERENCES report(id)
  ON DELETE CASCADE
);
"""

t2 = """CREATE TRIGGER pdf_timestamp AFTER UPDATE ON pdf
    BEGIN
      UPDATE pdf
         SET modified = CURRENT_TIMESTAMP
       WHERE pdf_id = old.pdf_id;
    END;

"""

c3 = """CREATE TABLE pdf_in_report (
  report_id varchar(8),
  pdf_id INTEGER,
  num int8,
  modified DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(report_id) REFERENCES report(id)
  ON DELETE CASCADE,
  FOREIGN KEY(pdf_id) REFERENCES pdf(pdf_id)
  ON DELETE CASCADE
  PRIMARY KEY (report_id, pdf_id)
);
"""

t3 = """CREATE TRIGGER pdf_in_report_timestamp AFTER UPDATE ON pdf_in_report
    BEGIN
      UPDATE pdf_in_report
         SET modified = CURRENT_TIMESTAMP
       WHERE pdf_id = old.pdf_id
         AND report_id = old.report_id;
    END;

"""

c4 = """CREATE TABLE section (
  report_id varchar(8),
  section_id INTEGER PRIMARY KEY,
  name varchar(256),
  slides TEXT,
  pdf_num int8,
  icon_path TEXT,
  modified datetime default current_timestamp,
  FOREIGN KEY(report_id) REFERENCES report(id)
  ON DELETE CASCADE
);
"""

t4 = """CREATE TRIGGER section_timestamp AFTER UPDATE ON section
    BEGIN
      UPDATE section
         SET modified = CURRENT_TIMESTAMP
       WHERE section_id = old.section_id;
    END;

"""

c5 = """CREATE TABLE hyperlink (
  report_id varchar(8),
  hyperlink_id INTEGER PRIMARY KEY,
  name varchar(8),
  slide_num int8,
  pdf_num int8,
  modified datetime default current_timestamp,
  FOREIGN KEY(report_id) REFERENCES report(id)
  ON DELETE CASCADE
);
"""

t5 = """CREATE TRIGGER hyperlink_timestamp AFTER UPDATE ON hyperlink
    BEGIN
      UPDATE hyperlink
         SET modified = CURRENT_TIMESTAMP
       WHERE hyperlink_id = old.hyperlink_id;
    END;
"""

i1 = """INSERT INTO report (id, name)
VALUES ('1', 'Report 1'),
       ('2', 'Report 2'),
       ('3', 'Report 3'),
       ('4', 'Report 4');
"""

i2 = """INSERT INTO pdf (report_id, num, refresh_interval_ms, file_name)
VALUES ('1', 1, '3600', 'blabla.pdf'),
       ('1', 2, '3600', 'new.pdf'),
       ('2', 1, '18000', 'blabla.pdf'),
       ('2', 2, '7200', 'new.pdf'),
       ('3', 1, '7200', 'old.pdf'),
       ('3', 2, '7200', 'new.pdf');
"""

i3 = """INSERT INTO pdf_in_report (report_id, pdf_id, num)
VALUES ('1', '1', 1),
       ('1', '2', 2),
       ('2', '1', 1),
       ('2', '2', 2),
       ('3', '1', 1);
"""

i4 = """INSERT INTO section (report_id, name, slides, pdf_num, icon_path)
VALUES ('1', 'Weekly', '[1, 2, 3]', 1, '/icons/1.svg'),
       ('1', 'Realtime', '[1, 2, 3]', 1, '/icons/1.svg'),
       ('2', 'Weekly', '[1, 2, 3]', 1, '/icons/1.svg'),
       ('2', 'Realtime', '[1, 2, 3]', 1, '/icons/1.svg'),
       ('3', 'Weekly', '[1, 2, 3]', 1, '/icons/1.svg'),
       ('3', 'Realtime', '[1, 2, 3]', 1, '/icons/1.svg');

"""

i5 = """INSERT INTO hyperlink (report_id, name, slide_num, pdf_num)
VALUES ('1', 'mos.ru', 1, 1),
       ('1', 'mos.ru', 2, 1),
       ('2', 'mos.ru', 1, 1),
       ('2', 'mos.ru', 2, 1),
       ('3', 'mos.ru', 1, 1),
       ('3', 'mos.ru', 2, 1);
"""

queries = [c1, t1, c2, t2, c4, t4, c5, t5, i1, i2, i4, i5]

def main():
    os.remove(database)
    open(database, 'a').close()
    connection = sqlite3.connect(database)
    for query in queries:
        print(query)
        connection.execute(query)
    connection.commit()
    print('Done.')

if __name__ == "__main__":
    main()
