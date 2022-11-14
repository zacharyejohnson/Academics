
/**
 *
 * @author Zach Johnson
 * @version 9/2/2021
 * The salaried class is a subclass of employee that holds salaried employee objects 
 */
public class Salaried extends Employee {
    private String title;
    private int salary;
    private static int salariedCount; 
    
    /**
     * 
     * @param id
     * @param name
     * @param title
     * @param salary 
     */
    public Salaried( int id, String name, String title, int salary )
    {
        super( id, name );
        this.title = title;
        this.salary = salary;
        salariedCount++; 
    }
    
    /**
     * 
     * @return title of salaried employee 
     */
    public String getTitle( ) { return title; }
    
    /**
     * 
     * @param title updates title
     */
    public void setTitle( String title ) { this.title = title; }
    
    
  /**
    @return Salary of Salaried employee 
    */
    public int getSalary( ) { return salary; }
    
    /**
     * 
     * @param salary updates salary
     *@Override
     */
    public void setSalary( int salary ) { this.salary = salary; }
    
    /**
    @return # of salaried workers
    */
    public static int getSalariedCount(){
        return salariedCount; 
    }
    
    /**
     * 
     * @return contents of instance
     */
    public String toString()
    {
        return super.toString() + ":" + getClass().getName() + "@" + title + ":" + salary;
    }
    
    /**
     * 
     * @param o
     * @return true if equal, false otherwise
     */
    public boolean equals( Object o )
    {
        if ( !( o instanceof Salaried ) )
            return false;
        
        Salaried s = ( Salaried ) o;
        
        return super.equals( s )
                && title.equals( s.title )
                && salary == s.salary;
    }    
}
