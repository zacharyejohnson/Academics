
import java.util.InputMismatchException;
/**
 *
 * @author Zach Johnson
 */
public class StandingComparator {
    public static int compare(Student a, Student b) throws NullPointerException{
        if( a == null || b == null )
            throw new NullPointerException("Student object null"); 
        
        int returnValue = 0;
        
        String aStanding = a.getStanding();
        String bStanding = b.getStanding();      
        
        switch ( aStanding )
        {
            case "freshman" : 
            {
                switch ( bStanding )
                {
                    case "freshman"   : returnValue = 0; break;                    
                    case "sophomore" : returnValue = -1; break;
                    case "junior" : returnValue = -1; break;   
                    case "senior" : returnValue = -1; break; 
                } 
                break;
            }
            case "sophomore" :
            {
                switch ( bStanding )
                {
                    case "freshman"   : returnValue = 1; break;                    
                    case "sophomore" : returnValue = 0; break;
                    case "junior" : returnValue = -1; break;   
                    case "senior" : returnValue = -1; break;
                }
                break;
            }
            case "junior" :
            {
                switch ( bStanding )
                {
                    case "freshman"   : returnValue = 1; break;                    
                    case "sophomore" : returnValue = 1; break;
                    case "junior" : returnValue = 0; break;   
                    case "senior" : returnValue = -1; break;
                }      
                break;
            }
            case "senior" :
            {
                switch ( bStanding )
                {
                    case "freshman"   : returnValue = 1; break;                    
                    case "sophomore" : returnValue = 1; break;
                    case "junior" : returnValue = 1; break;   
                    case "senior" : returnValue = 0; break;
                }      
                break;
            }
            default :
            {
               throw new InputMismatchException("Not a real standing"); 
            }            
        }
        
        return returnValue;
    }            

    }   

