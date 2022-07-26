/* Enroll.java
 */

package csci366finalproject;
import java.util.ArrayList; 
/**
 *
 * @author Zach J 
 * The Enrolls class represents the relationship between Student and Class in a CSCI Department database management system
 * This was developed as part of Group 15's CSCI366 final project
 */
public class Enroll {
    
    CompositeKey enrollKey; 
    char letterGrade = '0';
    double numericGrade = 0; 

    public Enroll(CompositeKey enrollKey, char letterGrade, double numericGrade) {
        this.enrollKey = enrollKey;
        this.letterGrade = letterGrade;
        this.numericGrade = numericGrade;
    }
    
    public ArrayList<Student> getClassRoster(){
        
        ArrayList<Student> classRoster = new ArrayList<>(); 
        String classID = Integer.toString(enrollKey.getCourseId()); 
        // id[], fname[], lname[] = "SELECT student_id, fname, lname FROM student JOIN ON enrolls.enrollKey(student_id) = student.student_ID WHERE course_id = {classID}"; 
        
      //  for(i = 0; i++; i<id.length()){
       //    classRoster.add(new Student(id[i], fname[i], lname[i])); 
       // }
        return classRoster; 
}

    public void setEnrollKey(CompositeKey enrollKey) {
        this.enrollKey = enrollKey;
    }

    public void setLetterGrade(char letterGrade) {
        this.letterGrade = letterGrade;
    }

    public void setNumericGrade(double numericGrade) {
        this.numericGrade = numericGrade;
    }

    public CompositeKey getEnrollKey() {
        return enrollKey;
    }

    public char getLetterGrade() {
        return letterGrade;
    }

    public double getNumericGrade() {
        return numericGrade;
    }
    
    
    
    
}