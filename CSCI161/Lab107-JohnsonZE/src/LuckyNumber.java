import java.util.Objects;
import java.util.Random; 
/**
 *
 * @author Zach Johnson
 */
public class LuckyNumber {
    private String name;
    private int luckyNumber;
    
    /**
     * 
     * @param name the name of the lucky number
     */
    public LuckyNumber(String name) {
        this.name = name;
        Random rand = new Random();
        luckyNumber = rand.nextInt(10);
    }
    
    /**
     * 
     * @return the name associated with the LuckyNumber
     */
    public String getName() {
        return name;
    }
    public boolean isEven(LuckyNumber ln){
       int i = ln.getLuckyNumber();
        return (i % 2) == 0; 
    }
    public boolean isPrime(LuckyNumber ln){
        int i = ln.getLuckyNumber();
        boolean isPrime = true; 
        for(int j = 2; j < i; i++){
            if( (i % j) == 0)
                isPrime = false;  
        }
        return isPrime; 
    }
    
    /**
     * 
     * @return the lucky number
     */
    public int getLuckyNumber() {
        return luckyNumber;
    }
    
    /**
     * 
     * @return a string representation of the the LuckyNumber
     */
    public String toString() {
        return getClass().getName() + "@" + name + ":" + luckyNumber;
    }
    
    /**
     * 
     * @param o any object
     * @return true if the two objects have identical content
     */
    public boolean equals(Object o) {
        if (!(o instanceof LuckyNumber)) {
            return false;
        }
        LuckyNumber ln = (LuckyNumber) o;
        return luckyNumber == ln.luckyNumber && name == ln.name;
    }
}
