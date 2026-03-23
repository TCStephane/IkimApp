create table if not exists members(
    member_id integer primary key autoincrement,
    member_name text not null,
    date_added text not null,
    email text not null unique,
    phone text not null unique
    );

create table if not exists contributions(
    contribution_id integer primary key autoincrement,
    member_id integer not null,
    amount real not null,
    payment_type text not null,
    date text not null,
    foreign key (member_id) references members(member_id)
);