/**
 *
 * @author Zach Johnson
 * @version 9/1/2021
 * this is the main class that implements, uses, and tests our created classes 
 */
public class Client {

    /**
     * @param args the command line arguments
     */
  
   
    
    public static void main(String[] args) {
        // TODO code application logic here
          Employee[] employeeList = new Employee[10];
          double raisedHourlyRate = 0;
          int raisedSalary = 0;  
        // Creation of employee list and employees with their respective instance variables
      
   Employee employee1 = new Salaried( 1234567, "Al", "manager", 60000 );
    Employee employee2 = new Hourly( 23456789, "Kelly", "Hostess", 25.75 );  
    Employee employee3 = new Salaried( 34567891, "Peggy", "CEO", 120000 );
    Employee employee4 = new Hourly( 45678910, "Bud", "Busboy", 15.00 );
    Employee employee5 = new Hourly(7891011, "Marcy", "Server", 10.00);
    Employee employee6 = new Hourly( 56789101, "Jefferson", "Cook", 35.00 );
    
    //population of the array with created employees
    employeeList[0] = employee1; 
   employeeList[1] = employee2;
   employeeList[2] = employee3;
   employeeList[3] = employee4;
   employeeList[4] = employee5;
   employeeList[5] = employee6;
   
   //for loop to print contents of employeeList
   for(int i = 0; i < employeeList.length; i++){
          System.out.println(employeeList[i]);
}
   //for loop to give each employee 25% raise 
  for(int i = 0; i<employeeList.length; i++){
      //iterates only if the object at array position i is an Hourly object
      if(employeeList[i] instanceof Hourly ){
                raisedHourlyRate = ((Hourly)employeeList[i]).getHourlyRate() * 1.25;       
               ((Hourly)employeeList[i]).setHourlyRate(raisedHourlyRate);
               System.out.println(employeeList[i]);
      }
      //iterates only if the object at array position i is a salaried object
      else if(employeeList[i] instanceof Salaried){
            raisedSalary = (int) (((Salaried)employeeList[i]).getSalary() * 1.25); 
             ((Salaried)employeeList[i]).setSalary(raisedSalary); 
                System.out.println(employeeList[i]);
  }
      //doesnt print if object at array position i is null
                else {
                        employeeList[i] = null;
                        } 
                        
                   
  }
   
   
   // TESTING EQUALS METHOD
  // instantiate new objects for testing
  Hourly hourly1 = new Hourly(1234567, "John", "laborer", 12.50); 
  Hourly hourly2 = new Hourly(7891011, "Marissa", "Secretary", 18.00);
  //test for method accuracy and display results 
 boolean resultHourlyTest1 = hourly1.equals(hourly2); 
        System.out.println("If equals method works, result should be false: "+ resultHourlyTest1);
 boolean resultHourlyTest2 = hourly1.equals(hourly1);
    System.out.println("If equals method works, result should be true: "+ resultHourlyTest2);
   
 //instantiate Salaried objects for testiing
    Employee salaried1 = new Salaried( 1234567, "Al", "manager", 60000 );
    Employee salaried2 = new Salaried( 4545112, "Bob", "accountant", 40000 );
     boolean resultSalariedTest1 = salaried1.equals(salaried2); 
        System.out.println("If equals method works, result should be false: "+ resultSalariedTest1);
 boolean resultSalariedTest2 = salaried1.equals(salaried1);
    System.out.println("If equals method works, result should be true: "+ resultSalariedTest2);
    }
    
}
