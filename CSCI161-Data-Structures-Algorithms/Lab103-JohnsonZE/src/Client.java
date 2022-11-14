import java.util.Random; 
/**
 *
 * @author Zachary Johnson
 * @version 9/16/2021
 * Client class instantiates Scores object and performs operations on them 
 */

public class Client {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        
       //Object of Type Scores using the overloaded constructor and pass the value 16
        Scores list1 = new Scores(16); 
        
        Random rand = new Random(); 
        
        // for loop to populate the list in Scores object with 32 random numbers between 
        // -10 and +10 inclusive
        System.out.print("List being populated...");
        for(int i = 0; i < 32; i++){
            list1.add(rand.nextInt(10+10+1)-10);
            System.out.print(".");
        }
      
        //Call toString( ) to print the contents of the Scores object.
        System.out.print("\nContents of Scores Object: ");
        System.out.println(list1.toString());
        
        //add( ) method to add the number 7 to Scores object
        list1.add(7);
        System.out.println("\nNumber 7 added to Scores Object ");
        //current size of the list in the Scores object
        System.out.println("\nCurrent Size: " + list1.getCurrentSize()); 
        
        //remove( ) method to randomly remove a number from Scores class
        list1.remove();
        System.out.println("\nRandom number removed from Scores Object ");
        
        //number at the 25th index position
        System.out.println("\nNumber at 25th index position: " + list1.get(25)); 
        
        // frequency that the number returned by the previous step occurs in Scores class
        System.out.println("\nHow often number at 25th index occurs in Scores: " 
               + list1.getFrequencyOf(list1.get(25)) );
        
        //overloaded remove method to remove the first 
        //occurrence of number at the 25th index position from Scores class
        list1.remove(25);
        System.out.println("\nInstances of 25 removed from list");
        
        //frequency that this number now occurs in Scores class
        System.out.println("\nFrequency of 25: " + list1.getFrequencyOf(25));
        
        //Check whether the array in Scores object contains the number 15
        System.out.println("\nDoes list contain number 15? It should be false: " + list1.contains(15) );
        
        //capacity of the array in the Scores object
        System.out.println("\nCapacity of the array in the Scores object: " + list1.getCurrentSize());
    }
    
}
