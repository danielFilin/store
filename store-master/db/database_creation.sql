CREATE DATABASE store;
use store;
CREATE TABLE categories(
name VARCHAR(255),
my_id int(10) not NULL AUTO_INCREMENT PRIMARY KEY
);
INSERT INTO categories (name) VALUES
('Food'),
('machinery'),
('toys');

select * from categories;
