/* Course.java
 */
package csci366finalproject;

 /*
 * @author Zach J 
 * The Course class represents a course within the CSCI department at NDSU
 * This was built as part of Group 15's final project for CSCI366
 */
public class Course {
    
    int courseID; 
    int facultyID; 
    int roomNumber; 
    int courseNumber; 
    String courseName; 
    String courseDescription; 
    int creditHours; 

    public Course(int courseID, int facultyID, int roomNumber, int courseNumber, String courseName, String courseDescription, int creditHours) {
        this.courseID = courseID;
        this.facultyID = facultyID;
        this.roomNumber = roomNumber;
        this.courseNumber = courseNumber;
        this.courseName = courseName;
        this.courseDescription = courseDescription;
        this.creditHours = creditHours;
    }
    

    public int getCourseID() {
        return courseID;
    }

    public int getFacultyID() {
        return facultyID;
    }

    public int getRoomNumber() {
        return roomNumber;
    }

    public int getCourseNumber() {
        return courseNumber;
    }

    public String getCourseName() {
        return courseName;
    }

    public String getCourseDescription() {
        return courseDescription;
    }

    public int getCreditHours() {
        return creditHours;
    }

    public void setCourseID(int courseID) {
        this.courseID = courseID;
    }

    public void setFacultyID(int facultyID) {
        this.facultyID = facultyID;
    }

    public void setRoomNumber(int roomNumber) {
        this.roomNumber = roomNumber;
    }

    public void setCourseNumber(int courseNumber) {
        this.courseNumber = courseNumber;
    }

    public void setCourseName(String courseName) {
        this.courseName = courseName;
    }

    public void setCourseDescription(String courseDescription) {
        this.courseDescription = courseDescription;
    }

    public void setCreditHours(int creditHours) {
        this.creditHours = creditHours;
    }
    
    
}