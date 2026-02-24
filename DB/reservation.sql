use doghotel;

create table reservation (
	res_id int auto_increment primary key,
	room_num int not null,
    master_name varchar(20) not null,
    dog_name varchar(20) not null,
    start_date datetime not null,
    end_date datetime not null
    );