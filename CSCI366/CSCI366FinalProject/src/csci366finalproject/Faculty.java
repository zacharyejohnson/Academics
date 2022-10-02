//* Faculty.java
 
package csci366finalproject;
import java.time.LocalDateTime; 
import java.util.ArrayList; 
/**
 *
 * @author Zach J 
 * The Faculty class represents a faculty member within the CSCI department at NDSU
 * This was built as part of Group 15's final project for CSCI366
 */
public class Faculty {
    int facultyID; 
    String fname; 
    String lname; 
    String position; 
    String credential;
    LocalDateTime hireDate = LocalDateTime.now(); 

    public Faculty(int facultyID, String fname, String lname, String position, String credential, LocalDateTime hireDate) {
        this.facultyID = facultyID;
        this.fname = fname;
        this.lname = lname;
        this.position = position;
        this.credential = credential;
        this.hireDate = hireDate;
    }
    
    public ArrayList<Course> coursesTaught(){
        ArrayList<Course> coursesTaught = new ArrayList<>(); 
        // need sql implemented here
        return coursesTaught; 
    }
     
     public int yearsEmployed(){
         return LocalDateTime.now().getYear() - hireDate.getYear(); 
     }
        
    

    public int getFacultyID() {
        return facultyID;
    }

    public String getFname() {
        return fname;
    }

    public String getLname() {
        return lname;
    }

    public String getPosition() {
        return position;
    }

    public String getCredential() {
        return credential;
    }

    public LocalDateTime getHireDate() {
        return hireDate;
    }

    public void setFacultyID(int facultyID) {
        this.facultyID = facultyID;
    }

    public void setFname(String fname) {
        this.fname = fname;
    }

    public void setLname(String lname) {
        this.lname = lname;
    }

    public void setPosition(String position) {
        this.position = position;
    }

    public void setCredential(String credential) {
        this.credential = credential;
    }

    public void setHireDate(LocalDateTime hireDate) {
        this.hireDate = hireDate;
    }
    
    
    
}