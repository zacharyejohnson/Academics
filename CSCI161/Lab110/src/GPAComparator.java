/**
 *
 * @author Zach Johnson
 */
public class GPAComparator {
    public static int compare(Student a, Student b) throws NullPointerException{
        if( a == null || b == null )
            throw new NullPointerException("Student object null"); 
        
       int returnValue;
       double diff = a.getGpa()-b.getGpa(); 
       if(diff < 0)
               returnValue = -1; 
       else if(diff > 0)
           returnValue = 1; 
       else
           returnValue = 0; 
       return returnValue; 
}
}
