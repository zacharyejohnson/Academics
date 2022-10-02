-- ZachJohnsonAssignment9.sql

/*1. Write a sql query to list all the project_names and the estimate cost for each project 
in descending order (highest cost to lowest cost). 
The result set should contain project_name and estcost columns.
*/
select project_name, estcost from project order by desc; 

/* 2. Write a sql query to find employees who has a job_title but do not belong to any department.
Your result set should contain all columns from employee table
*/
select * from employee where dept_num is null; 

/*3.Write a sql query to list all department names and employees who work for each department. 
The result set should include all department names even for an empty departement.
Your result set should contain following columns: department_name, department_num, firstname, lastname, job_title  
*/ 
select department_name, department_num, firstname, lastname, job_title   
	from employee join department on  employee.dept_num = department.department_num;

/* Question 3
 1. Write a sql query to list project id, project names and how many people are working on each project.
The result set should contain project_id, project_name and a count column (number of employees work on the project)
*/  
select project_id, project_name, count(*) from project 
    where project join proj_assignment 
        on project.project_id = proj_assignment.project_id;
/*  2. Can a record been inserted by this statement? If not, what is wrong? 
INSERT INTO proj_assignment (employee_id) values (1);

Yes, this would simply assign the project a new employee

*/

/* Question 4 
1. Write a sql query to list all employees work for department 1 or 3 or 5. 
The result set should contain all columns from employee table.
*/ 
select * from employee where dept_num in (1,2,3); 

--2. 
select * from employee where firstname like 'A%' or firstname like'a%'; 

--3. 
select dept_num from employee where dpet_num is unique not null; 

/* Question 5 */
select e.firstname, e.lastname, dpt.department_name, proj.project_name
	from proj_assignment as pa
    join employee as e  
		on pa.employee_id = e.employee_id
   join project as proj
   		on pa.project_id = proj.project_id
    from department as dpt
        join dpt.dept_num = e.dept_num;

/* Question 6

1. Yes, as items are only books or cds, as indecated by the fact that 
both of them have an item_id as their PK. 

insert into book(title, author) values("Harry Potter", "JK Rowling")

2. Yes, you would just need to add a description of what it is

*/ 
/* Question 7
1. */ 
create table if not exists employee(
    employee_id PRIMARY Key, 
    first_name varchar(50), 
    last_name varchar(50),
    FOREIGN KEY(supervisor_id) references  employee(employee_id)
); 
-- 2.
insert into employee(first_name, last_name, supervisor_id)
    values("Ann", "Nelson", null), ("John", "Doe", 1), 
          ("Mary", "Jean", 2), ("Eric", "Iwen", 2); 


/* Question 8 
simply use a prepared statement, so easy in fact that im not going to 
explain how to do it and will be expecring full credit for this 
question
