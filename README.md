# team4Payroll
Repo for files regarding group 4 (payroll)


= DATABASE SETUP =

table name = employees

Database should have the following fields:
- INT AUTOINCR employee_number (this is the primary key for identifying employyees)
- VARCHAR NOT NULL forename
- VARCHAR NOT NULL surname
- VARCHAR NOT NULL email_address
- INT NOT NULL salery
- INT NOT NULL days_worked_this_month
- INT NOT NULL monthly_expenses (default = 0)


Example setup:

CREATE TABLE IF NOT EXISTS employees (
    employee_number INT AUTO_INCREMENT PRIMARY KEY,
    forename VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    email_address VARCHAR(255) NOT NULL,
    salary INT NOT NULL,
    days_worked_this_month INT NOT NULL,
    monthly_expenses INT NOT NULL DEFAULT 0);


Example insert:
INSERT INTO employees (forename, surname, email_address, salary, days_worked_this_month) VALUES
'name', 'name', 'email', 40000, 14);