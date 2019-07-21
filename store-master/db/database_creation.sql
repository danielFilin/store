CREATE DATABASE store;
use store;

CREATE TABLE categories(
id int(10) not NULL AUTO_INCREMENT PRIMARY KEY UNIQUE,
name VARCHAR(255)
);

INSERT INTO categories (name) VALUES
('Food'),
('machinery'),
('toys');


ALTER TABLE categories 
add unique (name);
select * from categories;

drop table categories
