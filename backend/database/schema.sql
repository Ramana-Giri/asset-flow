CREATE TABLE employees(
	employee_id SERIAL PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	email_address VARCHAR(255) UNIQUE NOT NULL,
	hashed_password VARCHAR(255) NOT NULL
);

CREATE TABLE assets(
	asset_id SERIAL PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	category VARCHAR(255) NOT NULL,
	status VARCHAR(255) NOT NULL DEFAULT 'not assigned'
	CHECK (status IN ('assigned', 'not assigned')),	
	assigned_to INT REFERENCES employees(employee_id)
);