PRAGMA foreign_keys = ON;

CREATE TABLE report (
  id varchar(8) PRIMARY KEY,
  name varchar(255)
);

CREATE TABLE pdf (
  id_pdf INTEGER PRIMARY KEY,
  id_report varchar(8),
  num int8,
  refresh_interval_ms int,
  path TEXT,
  FOREIGN KEY(id_report) REFERENCES report(id)
  ON DELETE CASCADE
);

CREATE TABLE section (
  id_section INTEGER PRIMARY KEY,
  id_report varchar(8),
  name varchar(256),
  slides TEXT,
  pdf_num int8,
  icon_path TEXT,
  FOREIGN KEY(id_report) REFERENCES report(id)
  ON DELETE CASCADE
);

CREATE TABLE hyperlink (
  id_hyperlink INTEGER PRIMARY KEY,
  id_report varchar(8),
  name varchar(8),
  slide_num int8,
  pdf_num int8,
  FOREIGN KEY(id_report) REFERENCES report(id)
  ON DELETE CASCADE
);

INSERT INTO report (id, name)
VALUES ('1', 'Report 1'),
       ('2', 'Report 2'),
       ('3', 'Report 3'),
       ('4', 'Report 4');

INSERT INTO pdf (id_report, num, refresh_interval_ms, path)
VALUES ('1', 1, '3600', 'blabla.pdf'),
       ('1', 1, '3600', 'new.pdf'),
       ('2', 1, '18000', 'blabla.pdf'),
       ('3', 1, '7200', 'new.pdf'),
       ('3', 1, '7200', 'old.pdf'),
       ('3', 1, '7200', 'new.pdf');

INSERT INTO section (id_report, name, slides, pdf_num, icon_path)
VALUES ('1', 'Weekly', '[1, 2, 3]', 1, '/icons/1.svg'),
       ('1', 'Realtime', '[1, 2, 3]', 1, '/icons/1.svg'),
       ('2', 'Weekly', '[1, 2, 3]', 1, '/icons/1.svg'),
       ('2', 'Realtime', '[1, 2, 3]', 1, '/icons/1.svg'),
       ('3', 'Weekly', '[1, 2, 3]', 1, '/icons/1.svg'),
       ('3', 'Realtime', '[1, 2, 3]', 1, '/icons/1.svg');

INSERT INTO hyperlink (id_report, name, slide_num, pdf_num)
VALUES ('1', 'mos.ru', 1, 1),
       ('1', 'mos.ru', 2, 1),
       ('2', 'mos.ru', 1, 1),
       ('2', 'mos.ru', 2, 1),
       ('3', 'mos.ru', 1, 1),
       ('3', 'mos.ru', 2, 1);

-- INSERT INTO section (id_section, id_report, name, slides, pdf_num, icon_path)
-- VALUES ('1', '1', 'Weekly', '[1, 2, 3]', 1, '/icons/1.svg'),
--        ('2', '1', 'Realtime', '[1, 2, 3]', 1, '/icons/1.svg'),
--        ('3', '2', 'Weekly', '[1, 2, 3]', 1, '/icons/1.svg'),
--        ('4', '2', 'Realtime', '[1, 2, 3]', 1, '/icons/1.svg'),
--        ('5', '3', 'Weekly', '[1, 2, 3]', 1, '/icons/1.svg'),
--        ('6', '3', 'Realtime', '[1, 2, 3]', 1, '/icons/1.svg');
--
-- INSERT INTO hyperlink (id_hyperlink, id_report, name, slide_num, pdf_num)
-- VALUES ('1', '1', 'mos.ru', 1, 1),
--        ('2', '1', 'mos.ru', 2, 1),
--        ('3', '2', 'mos.ru', 1, 1),
--        ('4', '2', 'mos.ru', 2, 1),
--        ('5', '3', 'mos.ru', 1, 1),
--        ('6', '3', 'mos.ru', 2, 1);
--
-- INSERT INTO pdf (id_pdf, id_report, num, refresh_interval_ms, path)
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
