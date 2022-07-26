/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package csci366finalproject;

/**
 *
 * @author Zach J 
 */
public class SQLInsert {
    
    String fname = facultyTextField1.getText(); 
    String lname = facultyTextField2.getText(); 
    String position = facultyTextField3.getText(); 
    String credential = facultyTextField4.getText(); 
    String hiredate = facultyTextField5.getText(); 
    
    String query = "INSERT INTO faculty(firstname, lastname, faculty_position, credential, hire_date)"
            + "VALUES('" +fname + "', '" + lname+"', '"+position+",'"+credential+"', '"+hiredate+"'"; 
    Statement stmt = new Satement(conn); 
    stmt.executeUpdate(query); 
    
}
