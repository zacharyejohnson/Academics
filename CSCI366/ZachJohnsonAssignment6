-- 1. 
select count(employee_id)
	from employee as num_employees;

-- 2. 
select count(employee_id) 
	from employee 
		where dept_num = 1; 

-- 3. 
select max(estcost), min(estcost), avg(estcost), sum(estcost) 
	from project as proj_cost_parameters; 

-- 4. 
select employee_id, firstname, lastname, job_title, dept_num from employee where job_title is not null; 

-- 5. 
select firstname, lastname, job_title, dept_num from employee where job_title is not null; 

-- 6. 
select firstname, lastname, job_title, dept_num from employee where dept_num in (1,2,3); 

-- 7. 
select * from project order by estcost ASC; 

-- 8. 
select * from employee where firstname like 'A%' or firstname like'a%' order by firstname; 

-- 9. 
select dept_num, firstname, count(*) from employee group by dept_num, firstname having dept_num is not null; 

-- 10. 
select dept_num, count(*) from employee group by dept_num having count(dept_num) >= 5; 

-- 11. 
select firstname, lastname, job_title, department_name from employee, department where department_name in ('IT', 'HR'); 

-- 12. 
select firstname, lastname, dept_num, department_name 
	from employee join department on  employee.dept_num = department.department_num 
			where dept_num is not null; 
-- 13. 
select firstname, lastname, dept_num, department_name 
	from employee left join department  
		on employee.dept_num = department.department_num; 
		
-- 14. 
select firstname, lastname, dept_num, department_name 
	from employee right join department  
		on employee.dept_num = department.department_num;
		
-- 15.
select e.firstname, e.lastname, pa.project_id, proj.project_name
	from proj_assignment as pa
    join employee as e  
		on pa.employee_id = e.employee_id
   join project as proj
   		on pa.project_id = proj.project_id; 

 -- 16. 
select e.firstname, e.lastname, pa.project_id, proj.project_name, proj.estcost
	from proj_assignment as pa
    join employee as e  
		on pa.employee_id = e.employee_id
   join project as proj
   		on pa.project_id = proj.project_id
		where estcost > 50000 order by estcost asc; 
		
-- 17. 
select employee_id from employee_with_reward1
union
select employee_id from employee_with_reward2
union
select employee_id from employee_with_reward3; 

-- 18. 
select employee_id, reward_year from employee_with_reward1
union
select employee_id, reward_year from employee_with_reward2; 

-- 19.
select employee_id, reward_year from employee_with_reward1 where reward_year = 2020
union
select employee_id, reward_year from employee_with_reward2 where reward_year = 2020; 

-- 20. 
select employee_id from employee_with_reward1
except
select employee_id from employee_with_reward2; 

-- 21. 
select employee_id from employee_with_reward2
except
select employee_id from employee_with_reward1; 

-- 22. 
update employee 
	set job_title = 'Senior STE' where firstname = 'Mike'; -- couldn't figure out how to do the apostrophe in O'reilly

-- 23.
update employee
	set job_title = 'unknown' where job_title is null; 
	
-- 24. 
update employee_with_reward3
	set stock_reward_amount = (stock_reward_amount + 5000) where reward_year = 2020; 
	
-- 25. 
/* delete from department; 
 ERROR:  update or delete on table "department" violates foreign key constraint "employee_dept_num_fkey" on table "employee"
DETAIL:  Key (department_num)=(1) is still referenced from table "employee". 
We cannot delete the department records because they are referenced in the employee tabel and this would ruin the employee table */ 
-- this command will delete any department record whith zero employees
delete from department where department_num not in (select dept_num from employee);  

-- 26.
select employee_id, firstname, lastname, job_title from employee
	where employee_id 
    in (select employee_id from employee_with_reward1) 
	and 
	employee_id in (select employee_id from employee_with_reward2)
	and 
	employee_id in (select employee_id from employee_with_reward1); 




 