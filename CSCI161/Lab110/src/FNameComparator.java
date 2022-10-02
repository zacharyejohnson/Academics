/**
 *
 * @author Zach Johnson
 */
public class FNameComparator {
     public static int compare(Student a, Student b) throws NullPointerException{
        if( a == null || b == null )
            throw new NullPointerException("Student object null"); 
        
        return a.getFname().compareTo(b.getFname()); 
     }
}
