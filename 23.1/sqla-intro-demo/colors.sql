-- from the terminal run:
-- psql < colors.sql

DROP DATABASE IF EXISTS colors;

CREATE DATABASE colors;

\c colors

CREATE TABLE colors
(
  id SERIAL PRIMARY KEY,
  name TEXT
);

INSERT INTO colors (name) VALUES ('red'), ('blue'), ('green');

BEGIN TRANSACTION;
  DELETE FROM colors;
  SELECT * FROM colors; 
  -- no colors are left!
ROLLBACK;

SELECT * FROM colors;
-- all the colors are still here!
-- we only removed them in a rolled back transaction.

BEGIN TRANSACTION;
  DELETE FROM colors;
  SELECT * FROM colors; 
  -- no colors are left!
COMMIT;

SELECT * FROM colors;
-- Since we committed the transaction,
-- all of the colors are gone.