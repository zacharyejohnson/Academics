import java.io.*; 
import java.util.Arrays;
import java.util.Random; 
import java.io.File; 
import java.util.Scanner;

/**
 *
 * @author Zach Johnson
 * @version 12/3/2021
 */
public class Client {
    
 /** Merge contents of arrays S1 and S2 into properly sized array S. */
  public static <K> void merge(K[ ] S1, K[ ] S2, K[ ] S) {
   int i = 0, j = 0;
   while (i + j < S.length) {
     if (j == S2.length || (i < S1.length && ((int)S1[i] - (int)S2[j] < 0)))
        S[i+j] = S1[i++];               // copy ith element of S1 and increment i
     else
        S[i+j] = S2[j++];                // copy jth element of S2 and increment j
   }
 }



 /** Merge-sort contents of array S. */
 public static <K> void mergeSort(K[ ] S) {
   int n = S.length;
   if (n < 2) return;                              // array is trivially sorted
   // divide
   int mid = n/2;
   K[ ] S1 = Arrays.copyOfRange(S, 0, mid);         // copy of first half
  K[ ] S2 = Arrays.copyOfRange(S, mid, n);         // copy of second half
  // conquer (with recursion)
  mergeSort(S1);                            // sort copy of first half
   mergeSort(S2);                            // sort copy of second half
   // merge results
   merge(S1, S2, S);              // merge sorted halves back into original
 }
        
        private static final int MAX_VALUE = 200000000; 
        private static final int MIN_VALUE = 0; 
        private static Random rand = new Random(); 

public static long externalMergeSort(File inputFile, File outputFile) throws FileNotFoundException, IOException{
    long ram = Runtime.getRuntime().maxMemory();
    long fileSize = inputFile.length();
    int numBlocks = (int)(fileSize / ram) ; 
    Scanner scan = new Scanner(inputFile); 
   
    LinkedStack<Object[]> blocks = new LinkedStack<>();
    long start = System.currentTimeMillis(); 
    for (int j = 0; j< numBlocks; j++){
        Object[] tempArray = new Object[(int)(fileSize / 4)/numBlocks];
     for (int i = 0; i < ((fileSize / 4)/numBlocks); i++){ // 4 bytes per int
         while(scan.hasNext()){
         String next = scan.nextLine(); 
         tempArray[i] = next; 
        }
     }
     mergeSort(tempArray);
     blocks.push(tempArray);
    }
    long end = System.currentTimeMillis(); 
    long time = start-end; 
    
    PrintWriter pwOut = new PrintWriter(new FileWriter(outputFile), true);
        while(!blocks.isEmpty()){
           Object[] current = blocks.pop(); 
            for (Object c : current) {
                pwOut.println(c);
             }
         }
            
    return time; 
}
    /**
     * @param 
     */
    public static void main(String[] args) throws IOException {
       File inputFile = new File("C:\\data\\data.txt"); 
       File outputFile = new File("C:\\data\\dataSorted.txt"); 
       
       // generate input data
          PrintWriter pw = new PrintWriter(new FileWriter(inputFile), true);
         long start = System.currentTimeMillis(); 
         for(int i=0; i<2000;i++ ){
             int x = rand.nextInt(Client.MIN_VALUE, Client.MAX_VALUE);
            pw.println(x);
         }
         long end = System.currentTimeMillis(); 
         long timeToGenInput = end-start; 
         System.out.println("Time to produce : " + timeToGenInput);
         
         long emsTime = externalMergeSort(inputFile, outputFile); 
         System.out.println("Time to external merge sort: "+emsTime);
    }
    
}

