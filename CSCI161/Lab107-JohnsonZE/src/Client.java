import java.lang.Iterable;  
 import java.util.Iterator;
/**
 *
 * @author Zach Johnson
 */
public class Client {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
       LuckyNumberList luckyNumberList = new LuckyNumberList(); 
       
       luckyNumberList.addLuckyNumber(new LuckyNumber("Johnathan"));//1
       luckyNumberList.addLuckyNumber(new LuckyNumber("Julia"));    //2
       luckyNumberList.addLuckyNumber(new LuckyNumber("David"));    //3
       luckyNumberList.addLuckyNumber(new LuckyNumber("Jennifer")); //4
       luckyNumberList.addLuckyNumber(new LuckyNumber("Pablo"));    //5
       luckyNumberList.addLuckyNumber(new LuckyNumber("Sydney"));   //6
       luckyNumberList.addLuckyNumber(new LuckyNumber("Carl"));     //7
       luckyNumberList.addLuckyNumber(new LuckyNumber("Megan"));    //8
       luckyNumberList.addLuckyNumber(new LuckyNumber("Riley"));    //9
       luckyNumberList.addLuckyNumber(new LuckyNumber("Harper"));   //10
       

        
      System.out.println("Table with all lucky numbers");
        Iterable luckyNumberIterator = (Iterable<Position<LuckyNumber>>) luckyNumberList.positions();
        printIterableTable(luckyNumberIterator);

        System.out.println("\nTable with all the even lucky numbers");
        Iterable evenNumberIterator = (Iterable<Position<LuckyNumber>>) luckyNumberList.evenNumbers();
        printIterableTable(evenNumberIterator);
        
        System.out.println("\nTable with all the prime lucky numbers");
        Iterable primeNumberIterator = (Iterable<Position<LuckyNumber>>) luckyNumberList.primeNumbers();
        printIterableTable(primeNumberIterator);


    }
    
    /**
     * Prints a simple table with all the lucky numbers
     * @param lni the iterable lucky numbers
     */
    public static void printIterableTable(Iterable<Position<LuckyNumber>> lni) {
        System.out.printf("%-7s %-12s %-6s %-9s\n", "Name", "Lucky Number", "Parity", "Primality");
        for (Position<LuckyNumber> pln : lni) {
            LuckyNumber ln = pln.getElement();
            String even = LuckyNumberList.isEven(ln.getLuckyNumber()) ? "Even" : "Odd";
            String prime = LuckyNumberList.isPrime(ln.getLuckyNumber()) ? "Prime" : "Not Prime";
            System.out.printf("%-7s %-12d %-6s %-9s\n", ln.getName(), ln.getLuckyNumber(), even, prime);  
        }
    }
    }
   
       
    

