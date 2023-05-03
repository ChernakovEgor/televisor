CREATE TABLE report (
  id_report varchar(8) PRIMARY KEY,
  name varchar(255)
);

CREATE TABLE pdf (
  id_pdf varchar(8) PRIMARY KEY,
  id_report varchar(8),
  num int8,
  refresh_interval_ms int,
  path TEXT,
  FOREIGN KEY(id_report) REFERENCES report(id_report)
);

CREATE TABLE section (
  id_section varchar(8) PRIMARY KEY,
  id_report varchar(8),
  section_name varchar(256),
  slides TEXT,
  pdf_num int8,
  icon_path TEXT
  FOREIGN KEY(id_report) REFERENCES report(id_report)
)

INSERT INTO report (id_report, name)
VALUES ('1', 'Report 1'),
       ('2', 'Report 2'),
       ('3', 'Report 3'),
       ('4', 'Report 4');

INSERT INTO pdf (id_pdf, id_report, num, refresh_interval_ms, path)
VALUES ('1', '1', 1, '3600', 'blabla.pdf'),
       ('2', '1', 1, '3600', 'new.pdf'),
       ('3', '2', 1, '18000', 'blabla.pdf'),
       ('4', '3', 1, '7200', 'new.pdf'),
       ('5', '3', 1, '7200', 'old.pdf'),
       ('6', '3', 1, '7200', 'new.pdf');


-- sleep ~ 8 sec
WITH RECURSIVE r(i) AS (
  VALUES(0)
  UNION ALL
  SELECT i FROM r
  LIMIT 50000000
)
SELECT i FROM r WHERE i = 1;
