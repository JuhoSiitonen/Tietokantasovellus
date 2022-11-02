
CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
	name TEXT UNIQUE,
	password TEXT,
	address TEXT,
	admin BOOLEAN,
	created_at TIMESTAMP
);

CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
	name TEXT UNIQUE,
	visible BOOLEAN,
	address TEXT
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
	restaurant_id INTEGER REFERENCES restaurants,
	dishes TEXT,
	price INTEGER,
	additional_info TEXT
);

CREATE TABLE dishes (
    id SERIAL PRIMARY KEY,
	restaurant_menu INTEGER REFERENCES restaurants,
	name TEXT,
	description TEXT,
	visible BOOLEAN,
	price INTEGER
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
	user_id INTEGER UNIQUE REFERENCES users,
	restaurant_id INTEGER UNIQUE REFERENCES users,
	stars INTEGER,
	review TEXT,
	visible BOOLEAN,
	time_given TIMESTAMP
);
