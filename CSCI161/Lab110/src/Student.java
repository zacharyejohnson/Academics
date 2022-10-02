import java.util.Random; 
import java.lang.StringBuilder; 

/**
 *
 * @author Zach Johnson
 */
public class Student{
   
    private int id; 
    private String lname; 
    private String fname; 
    private String standing; 
    private double gpa; 
  
    Random rand = new Random();
    
    public Student(){
        id = rand.nextInt(0, 9999999); 
        lname = getRandString(10, 15); 
        fname = getRandString(5, 10); 
        standing = getStanding(); 
        gpa = getGPA(); 
    } 
    protected double getGPA(){
        double gpa; 
      int randNum = rand.nextInt(0, 100); 
        if( randNum < 5)
            gpa = 4.00; 
        else if( randNum < 25 )
            gpa = rand.nextDouble(3, 4); 
        else if( randNum < 75)
            gpa = rand.nextDouble(2, 3); 
        else if( randNum < 95 )
            gpa = rand.nextDouble(1, 2); 
        else
            gpa = rand.nextDouble(0, 1); 
         
        return gpa; 
    }
   
    protected String getStanding(){
        int rndNumber = rand.nextInt(0, 10);
        if( rndNumber == 0)
            return "senior"; 
        else if( rndNumber < 3)
            return "junior"; 
        else if( rndNumber < 6 )
            return "sophomore"; 
        else
            return "freshman";  
    }
     String CHARS = "abcdefghijklmnopqrstuvwxyz";
        StringBuilder randString = new StringBuilder();
        Random rnd = new Random(); 
  
    protected String getRandString(int n, int k) { // n is the desired length of the random string
       int stringLength = rand.nextInt(n, k+1); 
        while (randString.length() < stringLength) { // length of the random string.
            int index = (int) (rnd.nextFloat() * CHARS.length());
            randString.append(CHARS.charAt(index));
        }
        String randStr = randString.toString();
        String first = randStr.substring(0,1); 
        randStr.replace(first, first.toUpperCase()); 
        return randStr;

    }
    public int getId() {
        return id;
    }

    public String getLname() {
        return lname;
    }

    public String getFname() {
        return fname;
    }

    public double getGpa() {
        return gpa;
    }
    /**
     * 
     * @return a comparator for employee's id
     */
    public static Comparator<Student> compareById() {
        return (Student s1, Student s2) -> s1.id - s2.id;
    }
    
    /**
     * 
     * @return a comparator for student's L name
     */
    public static Comparator<Student> compareByLName() {
        return (Student s1, Student s2) -> LNameComparator.compare(s1, s2);
    }
    /**
     * 
     * @return a comparator for student's F name
     */
    public static Comparator<Student> compareByFName() {
        return (Student s1, Student s2) -> FNameComparator.compare(s1, s2);
    }
    
    /**
     * 
     * @return a comparator for students standing
     */
    public static Comparator<Student> compareByStanding() {
        return (Student s1, Student s2) ->
                StandingComparator.compare(s1, s2); 
    }
    
    /**
     * 
     * @return a comparator for employee's hired
     */
    public static Comparator<Student> compareByGPA() {
        return (Student s1, Student s2) -> (int) (s1.getGpa() - s2.getGpa());
    }

    
}
