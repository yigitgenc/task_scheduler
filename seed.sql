CREATE TABLE IF NOT EXISTS pending_photos (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "filename" text NOT NULL,
  "status" integer(1) NOT NULL DEFAULT 0
);

INSERT INTO pending_photos(filename)
VALUES
  ('example1.jpg'),
  ('example2.jpg'),
  ('example3.jpg'),
  ('example4.jpg'),
  ('example5.jpg'),
  ('example6.jpg'),
  ('example7.jpg'),
  ('example8.jpg'),
  ('example9.jpg'),
  ('example10.jpg');
