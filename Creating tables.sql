create table Users
(
	id serial,
	user_name varchar(30) not null,
	user_mobile char(10) not null unique,
	account_number char(12) primary key,
	card_number varchar(10) not null unique,
	account_type varchar(15) not null,
	curr_balance decimal(12,2)
);

create table passwords
(
	id serial,
	password varchar(200) not null,
	account_number varchar(15) references Users(account_number),
	card_number varchar(10) references Users(card_number)
);

create table transactions
(
	id serial,
	account_number varchar(15) references Users(account_number),
	transaction_date timestamp default current_timestamp,
	type_of_transaction varchar(20) not null,
	amount_of_transaction decimal(12,2),
	curr_amount decimal(12,2)
);