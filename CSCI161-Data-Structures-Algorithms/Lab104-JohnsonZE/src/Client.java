/**
 * The client class tests our newly created ArrayBag and LinkedBag classes 
 * @author Zach Johnson
 * @version 9/24/2021
 */
public class Client {
    /**
     * Method called when program runs
     * @param args command line arguments 
     */
    public static void main(String[] args) {
  
    ArrayBag<Player> mensTeam = new ArrayBag<>(2); 
    
    // adding hardcoded players
    mensTeam.add(new Player("ZACH MATHIS", "WIDE RECEIVER", 0)); 
    mensTeam.add(new Player("CHRISTIAN WATSON", "WIDE RECEIVER", 1));
    mensTeam.add(new Player("QUINCY PATTERSON", "QUARTERBACK", 2));
    mensTeam.add(new Player("KOBE JOHNSON", "RUNNING BACK", 4));
    mensTeam.add(new Player("BRYCE LANCE", "WIDE RECEIVER", 5));
    mensTeam.add(new Player("CAM MILLER", "QUARTERBACK", 7));
    mensTeam.add(new Player("MITCHELL KARTES", "RUNNING BACK", 8));
    mensTeam.add(new Player("PHOENIX SPROLES", "WIDE RECEIVER", 11));
    
    // display contents of mensTeam
    System.out.println(mensTeam);
    
    // removal of random player 
    mensTeam.remove(); 
    
    // display contents again
    System.out.println(mensTeam);
    
    //Get but do not remove a reference to the 5th item in the bag
    Player a = mensTeam.get(5); 
        
    // contents from previouys step 
        System.out.println(a);
    
    //add another hardcoded player 
    mensTeam.add(new Player("BRAYLON HENDERSON", "WIDE RECEIVER", 12));
    
    // display contents
    System.out.println(mensTeam);
    
    // remove player gotten in step 5 
    mensTeam.remove(a); 
    
    //display
    System.out.println(mensTeam);
        
    // demonstration that my generic class can hold can support objects of different types 
    ArrayBag<String> courses = new ArrayBag<>(); 
       courses.add("CSCI 161"); 
       courses.add("STAT 367"); 
       courses.add("ECON 411"); 
       courses.add("Econ 201"); 
       courses.add("TL 116"); 
       
       // display courses
        System.out.println(courses);
        
        // remove random course 
        courses.remove(); 
        
        // display again 
        System.out.println(courses);
        
    // repeating steps 1 through 9 but using the LinkedBag class to demonstrate that the client 
    // can use either 
    
    LinkedBag<Player> womensTeam = new LinkedBag<>(); 
    womensTeam.add(new Player("RENEYA HOPKINS", "GUARD", 0));
    womensTeam.add(new Player("KYLIE STROP", "GUARD", 2)); 
    womensTeam.add(new Player("KADIE DEATON", "GUARD", 3)); 
    womensTeam.add(new Player("RYAN COBBINS", "FORWARD", 5)); 
    womensTeam.add(new Player("HEAVEN HAMLING", "GUARD", 11 ));
    womensTeam.add(new Player("MARIE OLSON", "FORWARD", 12)); 
    womensTeam.add(new Player("RACHEL NOVAK", "GUARD", 13)); 
    womensTeam.add(new Player("OLIVIA SKIBIEL", "FORWARD", 23)); 
    //display
   System.out.println(womensTeam);
   //remove random 
   womensTeam.remove(); 
   //display
    System.out.println(womensTeam);
    // get object at index 5
    Player b = womensTeam.get(5); 
    //display b 
    System.out.println(b);
    // add another player 
    womensTeam.add(new Player("ABBY SCHULTE", "GUARD", 24)); 
    //display
    System.out.println(womensTeam);
    // remove b
    womensTeam.remove(b); 
        
    
   
        
    
    
    }
}
