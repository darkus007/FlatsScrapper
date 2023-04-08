BEGIN;

CREATE TABLE IF NOT EXISTS project (
    project_id integer NOT NULL PRIMARY KEY,
    city varchar(127) NOT NULL,
    name varchar(127) NOT NULL,
    url varchar(255) NULL,
    metro varchar(127) NULL,
    time_to_metro integer NULL,
    latitude double precision NULL,
    longitude double precision NULL,
    address varchar(255) NULL,
    data_created date NOT NULL,
    data_closed date NULL
);

CREATE TABLE IF NOT EXISTS flat (
    flat_id integer NOT NULL PRIMARY KEY,
    project_id integer NOT NULL,
    address varchar(255) NULL,
    floor integer NULL,
    rooms integer NULL,
    area double precision NULL,
    finishing boolean NULL,
    bulk varchar(127) NULL,
    settlement_date date NULL,
    url_suffix varchar(127) NOT NULL,
    data_created date NOT NULL,
    data_closed date NULL,
    FOREIGN KEY(project_id) REFERENCES project(project_id)
);

CREATE TABLE IF NOT EXISTS price (
    price_id integer NOT NULL PRIMARY KEY,
    benefit_name varchar(127) NULL,
    benefit_description varchar(255) NULL,
    price integer NOT NULL,
    meter_price integer NULL,
    booking_status varchar(15) NULL,
    data_created date NOT NULL,
    flat_id integer NOT NULL,
    FOREIGN KEY(flat_id) REFERENCES flats(flat_id)
    );

COMMIT;
