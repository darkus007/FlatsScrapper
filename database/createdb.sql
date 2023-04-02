create table if not exists projects (
    project_id integer primary key,
    city varchar(127),
    name varchar(127),
    url varchar(255),
    metro varchar(127),
    time_to_metro integer,
    latitude real,
    longitude real,
    address varchar(255),
    data_created timestamp,
    data_closed timestamp
);

create table if not exists flats (
    flat_id integer primary key,
    project_id integer,
    address varchar(255),
    floor integer,
    rooms integer,
    area  real,
    finishing boolean,
    bulk varchar(127),
    settlement_date timestamp,
    url_suffix varchar(127),
    data_created timestamp,
    data_closed timestamp,
    FOREIGN KEY(project_id) REFERENCES projects(project_id)
);

create table  if not exists prices (
    flat_id integer,
    benefit_name varchar(127),
    benefit_description varchar(255),
    price integer,
    meter_price integer,
    booking_status varchar(15),
    data_created timestamp,
    FOREIGN KEY(price_id) REFERENCES flats(flat_id)
);
