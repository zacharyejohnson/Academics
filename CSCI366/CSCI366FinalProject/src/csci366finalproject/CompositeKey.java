/* CompositeKey.java
 */

package csci366finalproject;

/**
 *
 * @author Zach J 
 */
public class CompositeKey {
    
// ID's from two linked entities
    int id1; 
    int id2; 

    public CompositeKey(int courseID, int studentID) {
        this.id1 = courseID;
        this.id2 = studentID;
    }

    public int getCourseId() {
        return id1;
    }

    public int getStudentId() {
        return id2;
    }

    public void setCourseId(int id1) {
        this.id1 = id1;
    }

    public void setStudentId(int id2) {
        this.id2 = id2;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        final CompositeKey other = (CompositeKey) obj;
        if (this.id1 != other.id1) {
            return false;
        }
        if (this.id2 != other.id2) {
            return false;
        }
        return true;
    }



}