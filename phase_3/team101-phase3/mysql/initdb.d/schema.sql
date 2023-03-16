CREATE TABLE city_info (
  postal_code int NOT NULL,
  city varchar(50) NOT NULL,
  longitude float NOT NULL,
  latitude float NOT NULL, 
  state varchar(2) NOT NULL,
  PRIMARY KEY (postal_code)
);

CREATE TABLE household(
  email varchar(50) NOT NULL,
  square_footage int NOT NULL,
  number_of_occupants int NOT NULL,
  number_of_bedrooms int NOT NULL,
  household_type varchar(50) NOT NULL,
  postal_code int NOT NULL,
  PRIMARY KEY (email),
  FOREIGN KEY (postal_code)
    REFERENCES city_info (postal_code)
);

CREATE TABLE phone_info (
  phone_number int NOT NULL,
  area_code int NOT NULL,
  phone_type varchar(50) NOT NULL,
  email varchar(50) NOT NULL,
  PRIMARY KEY (area_code, phone_number),
  FOREIGN KEY (email)
    REFERENCES household (email)
);

CREATE TABLE half_bathroom (
  email varchar(50) NOT NULL,
  bathroom_number int NOT NULL,
  number_of_sinks int NOT NULL,
  number_of_commodes int NOT NULL,
  number_of_bidets int NOT NULL,
  half_bath_name varchar(50) NOT NULL,
  PRIMARY KEY (email, bathroom_number),
  FOREIGN KEY (email)
    REFERENCES household (email)
);

CREATE TABLE full_bathroom (
  email varchar(50) NOT NULL,
  bathroom_number int NOT NULL,
  number_of_sinks int NOT NULL,
  number_of_commodes int NOT NULL,
  number_of_bidets int NOT NULL,
  number_of_bathtubs int NOT NULL,
  number_of_showers int NOT NULL,
  number_of_tub_showers int NOT NULL,
  is_primary_bathroom boolean NOT NULL,
  PRIMARY KEY (email, bathroom_number),
  FOREIGN KEY (email)
    REFERENCES household (email)
);

CREATE TABLE manufacturer (
  id int NOT NULL AUTO_INCREMENT,
  manufacturer_name varchar(50) NOT NULL,
  PRIMARY KEY (id)
);


create table appliance (
  appliance_number int not null,
  model varchar(50) not null,
  manufacturer_id int not null,
  email varchar(50) NOT NULL,
  appliance_type varchar(50) NOT NULL,
  PRIMARY KEY (email, appliance_number),
  FOREIGN KEY (email)
    REFERENCES household (email),
  FOREIGN KEY (manufacturer_id)
    REFERENCES manufacturer (id)
);

  
create table dryer (
  dryer_heat_source varchar(50) not null,
  appliance_number int not null,
  email varchar(50) NOT NULL,
  PRIMARY KEY (email, appliance_number),
  FOREIGN KEY (email, appliance_number)
    REFERENCES appliance (email, appliance_number)
);

create table fridge (
  fridge_type varchar(50) not null,
  appliance_number int not null,
  email varchar(50) NOT NULL,
  PRIMARY KEY (email, appliance_number),
  FOREIGN KEY (email)
    REFERENCES household (email),
  FOREIGN KEY (email, appliance_number)
    REFERENCES appliance (email, appliance_number)
);
  
create table tv (
  display_type varchar(50) not null,
  display_size float not null,
  max_resolution varchar(50) not null,
  appliance_number int not null,
  email varchar(50) NOT NULL,
  PRIMARY KEY (email, appliance_number),
  FOREIGN KEY (email, appliance_number)
    REFERENCES appliance (email, appliance_number)
);
  
create table washer (
  loading_type varchar(50) not null,
  appliance_number int not null,
  email varchar(50) NOT NULL,
  PRIMARY KEY (email, appliance_number),
  FOREIGN KEY (email)
    REFERENCES household (email),
  FOREIGN KEY (email, appliance_number)
    REFERENCES appliance (email, appliance_number)
);

create table cooktop (
  cooktop_heat_source varchar(50) not null,
  appliance_number int not null,
  email varchar(50) NOT NULL,
  PRIMARY KEY (email, appliance_number),
  FOREIGN KEY (email)
    REFERENCES household (email),
  FOREIGN KEY (email, appliance_number)
    REFERENCES appliance (email, appliance_number)
);
  
create table oven (
  oven_type varchar(50) not null,
  appliance_number int not null,
  email varchar(50) NOT NULL,
  PRIMARY KEY (email, appliance_number),
  FOREIGN KEY (email)
    REFERENCES household (email),
  FOREIGN KEY (email, appliance_number)
    REFERENCES appliance (email, appliance_number)
);
  
create table oven_heat (
  oven_heat_id int not null AUTO_INCREMENT,
  oven_heat_source varchar(50) not null,
  appliance_number int not null,
  email varchar(50) NOT NULL,
  PRIMARY KEY (oven_heat_id),
  FOREIGN KEY (email)
    REFERENCES household (Email),
  FOREIGN KEY (email, appliance_number)
    REFERENCES appliance (email, appliance_number)
);
