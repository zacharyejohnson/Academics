
/**
 *
 * @author Zach Johnson
 * @version 9/2/2021
 * the hourly class is a subclass of employee that contains unique fields of hourly rate and position
 */
public class Hourly extends Employee {
   private  String position; 
  private  double hourlyRate; 
   private  static int hourlyCount; 
   /**
     * 
     * @param id
     * @param name
     * @param position
     * @param hourlyRate 
     */
   
   public Hourly( int id, String name, String position, double hourlyRate){
       super(id, name); 
       this.position = position; 
       this.hourlyRate = hourlyRate; 
       hourlyCount++; 
       
}
/**
   @param position updates position of hourly worker
   */
    public void setPosition(String position) {
        this.position = position;
    }
/**
    @param hourlyRate sets hourly rate of hourly employee 
    */
    public void setHourlyRate(double hourlyRate) {
        this.hourlyRate = hourlyRate;
    }

    /**
    @param hourlyCount sets number of hourly employees 
    */
    public void setHourlyCount(int hourlyCount) {
        this.hourlyCount = hourlyCount;
    }
/** 
 * @return position of hourly employee   
    */
    public String getPosition() {
        return position;
    }
/**
 * @return hourly rate of Employee  
    */
    public double getHourlyRate() {
        return hourlyRate;
    }
/** 
 * @return gets number of employees that are paid hourly  
    */
    public static int getHourlyCount() {
        return hourlyCount;
    }
    /**
     * 
     * @return contents of instance
     */
    public String toString() {
        return super.toString() + ":" + getClass().getName() + "@" + position + ":" + hourlyRate;
    }
    
    /**
     * 
     * @param o
     * @return true if equal, false otherwise
     */
    public boolean equals( Object o){
        if ( !( o instanceof Hourly ) )
            return false;
        Hourly s = (Hourly) o; 
        return super.equals(s)
                && position.equals(s.position)
                && hourlyRate == s.hourlyRate; 
    }
}
