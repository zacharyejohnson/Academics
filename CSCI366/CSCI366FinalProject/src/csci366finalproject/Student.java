/* Student.java
 */
package csci366finalproject;

/**
 *
 * @author Zach J 
 * The Student class represents a student within the CSCI department at NDSU
 * This was built as part of Group 15's final project for CSCI366
 */

public class Student {

    int studentID; 
    String fName; 
    String lName; 
    String specialization; 
    String classStanding; 
    
    public Student(int studentID, String fName, String lName, String specialization, String classStanding) {
        this.studentID = studentID;
        this.fName = fName;
        this.lName = lName;
        this.specialization = specialization;
        this.classStanding = classStanding;
    }
    
    

    public int getStudentID() {
        return studentID;
    }

    public String getfName() {
        return fName;
    }

    public String getlName() {
        return lName;
    }

    public String getSpecialization() {
        return specialization;
    }

    public String getClassStanding() {
        return classStanding;
    }

    public void setStudentID(int studentID) {
        this.studentID = studentID;
    }

    public void setfName(String fName) {
        this.fName = fName;
    }

    public void setlName(String lName) {
        this.lName = lName;
    }

    public void setSpecialization(String specialization) {
        this.specialization = specialization;
    }

    public void setClassStanding(String classStanding) {
        this.classStanding = classStanding;
    }
    
}