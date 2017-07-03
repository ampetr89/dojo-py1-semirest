create database if not exists semirestful
;

use semirestful
;
create table if not exists users(
 id int primary key auto_increment,
 first_name varchar(100),
 last_name varchar(100),
 email varchar(100),
 created_at datetime not null default current_timestamp,
 updated_at datetime not null default current_timestamp
)
;

