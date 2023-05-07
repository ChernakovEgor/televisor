PRAGMA foreign_keys = ON;

CREATE TABLE report (
  id VARCHAR(8) PRIMARY KEY,
  name VARCHAR(255),
  modified DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER report_timestamp AFTER UPDATE ON report
    BEGIN
      UPDATE report
         SET modified = CURRENT_TIMESTAMP
       WHERE id = old.id;
    END;

CREATE TABLE pdf (
  pdf_id INTEGER PRIMARY KEY,
  refresh_interval_ms int,
  pdf_path TEXT,
  modified datetime default current_timestamp
);

CREATE TRIGGER pdf_timestamp AFTER UPDATE ON pdf
    BEGIN
      UPDATE pdf
         SET modified = CURRENT_TIMESTAMP
       WHERE pdf_id = old.pdf_id;
    END;

CREATE TABLE pdf_in_report (
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

CREATE TRIGGER pdf_in_report_timestamp AFTER UPDATE ON pdf_in_report
    BEGIN
      UPDATE pdf_in_report
         SET modified = CURRENT_TIMESTAMP
       WHERE pdf_id = old.pdf_id
         AND report_id = old.report_id;
    END;

CREATE TABLE section (
  section_id INTEGER PRIMARY KEY,
  report_id varchar(8),
  name varchar(256),
  slides TEXT,
  pdf_num int8,
  icon_path TEXT,
  modified datetime default current_timestamp,
  FOREIGN KEY(report_id) REFERENCES report(id)
  ON DELETE CASCADE
);

CREATE TRIGGER section_timestamp AFTER UPDATE ON section
    BEGIN
      UPDATE section
         SET modified = CURRENT_TIMESTAMP
       WHERE section_id = old.section_id;
    END;

CREATE TABLE hyperlink (
  hyperlink_id INTEGER PRIMARY KEY,
  report_id varchar(8),
  name varchar(8),
  slide_num int8,
  pdf_num int8,
  modified datetime default current_timestamp,
  FOREIGN KEY(report_id) REFERENCES report(id)
  ON DELETE CASCADE
);

CREATE TRIGGER hyperlink_timestamp AFTER UPDATE ON hyperlink
    BEGIN
      UPDATE hyperlink
         SET modified = CURRENT_TIMESTAMP
       WHERE hyperlink_id = old.hyperlink_id;
    END;

INSERT INTO report (id, name)
VALUES ('1', 'Report 1'),
       ('2', 'Report 2'),
       ('3', 'Report 3'),
       ('4', 'Report 4');

INSERT INTO pdf (refresh_interval_ms, pdf_path)
VALUES ('3600', 'blabla.pdf'),
       ('3600', 'new.pdf'),
       ('18000', 'blabla.pdf'),
       ('7200', 'new.pdf'),
       ('7200', 'old.pdf'),
       ('7200', 'new.pdf');

INSERT INTO pdf_in_report (report_id, pdf_id, num)
VALUES ('1', '1', 1),
       ('1', '2', 2),
       ('2', '1', 1),
       ('2', '2', 2),
       ('3', '1', 1);

INSERT INTO section (report_id, name, slides, pdf_num, icon_path)
VALUES ('1', 'Weekly', '[1, 2, 3]', 1, '/icons/1.svg'),
       ('1', 'Realtime', '[1, 2, 3]', 1, '/icons/1.svg'),
       ('2', 'Weekly', '[1, 2, 3]', 1, '/icons/1.svg'),
       ('2', 'Realtime', '[1, 2, 3]', 1, '/icons/1.svg'),
       ('3', 'Weekly', '[1, 2, 3]', 1, '/icons/1.svg'),
       ('3', 'Realtime', '[1, 2, 3]', 1, '/icons/1.svg');

INSERT INTO hyperlink (report_id, name, slide_num, pdf_num)
VALUES ('1', 'mos.ru', 1, 1),
       ('1', 'mos.ru', 2, 1),
       ('2', 'mos.ru', 1, 1),
       ('2', 'mos.ru', 2, 1),
       ('3', 'mos.ru', 1, 1),
       ('3', 'mos.ru', 2, 1);

-- INSERT INTO section (section_id, report_id, name, slides, pdf_num, icon_path)
-- VALUES ('1', '1', 'Weekly', '[1, 2, 3]', 1, '/icons/1.svg'),
--        ('2', '1', 'Realtime', '[1, 2, 3]', 1, '/icons/1.svg'),
--        ('3', '2', 'Weekly', '[1, 2, 3]', 1, '/icons/1.svg'),
--        ('4', '2', 'Realtime', '[1, 2, 3]', 1, '/icons/1.svg'),
--        ('5', '3', 'Weekly', '[1, 2, 3]', 1, '/icons/1.svg'),
--        ('6', '3', 'Realtime', '[1, 2, 3]', 1, '/icons/1.svg');
--
-- INSERT INTO hyperlink (hyperlink_id, report_id, name, slide_num, pdf_num)
-- VALUES ('1', '1', 'mos.ru', 1, 1),
--        ('2', '1', 'mos.ru', 2, 1),
--        ('3', '2', 'mos.ru', 1, 1),
--        ('4', '2', 'mos.ru', 2, 1),
--        ('5', '3', 'mos.ru', 1, 1),
--        ('6', '3', 'mos.ru', 2, 1);
--
-- INSERT INTO pdf (pdf_id, report_id, num, refresh_interval_ms, path)
-- VALUES ('1', '1', 1, '3600', 'blabla.pdf'),
--        ('2', '1', 1, '3600', 'new.pdf'),
--        ('3', '2', 1, '18000', 'blabla.pdf'),
--        ('4', '3', 1, '7200', 'new.pdf'),
--        ('5', '3', 1, '7200', 'old.pdf'),
--        ('6', '3', 1, '7200', 'new.pdf');


-- sleep ~ 8 sec
WITH RECURSIVE r(i) AS (
  VALUES(0)
  UNION ALL
  SELECT i FROM r
  LIMIT 50000000
)
SELECT i FROM r WHERE i = 1;
