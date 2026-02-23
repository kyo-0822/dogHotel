use dogHotel;

create table if not exists user_db (
	name varchar(10),
    email varchar(50) primary key,
    password varchar(50)
);