create database if not exists dogHotel default character set utf8;

use dogHotel;

create table if not exists room_info (
	room_num int primary key,
    state varchar(10) default 'empty'
);

insert into room_info (room_num, state) values 
(1, 'empty'), (2, 'empty'), (3, 'empty'), (4, 'empty'), (5, 'empty'),
(6, 'empty'), (7, 'empty'), (8, 'empty'), (9, 'empty'), (10, 'empty');