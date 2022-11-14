
/**
 *
 * @author Zach Johnson
 * @version 9/10/2021
 * The Client Class asks the user for a data file containing stock Quotes and analyzes it, giving summary statistics. 
 * 
 * 
 */
import java.io.File;  
import java.util.Scanner; 
import java.io.*;   

public class Client {
 
  
    /**
     * @param args the command line arguments
     * @throws java.io.FileNotFoundException
     */
     
    public static void main(String[] args) throws FileNotFoundException {
        // TODO code application logic here
       
       // prompt user for file path 
        System.out.println("Enter the absolute file path (ex.\"C:\\data\\Lab102data.txt\") that includes the full Qoute of your stock data:");
        Scanner scan = new Scanner(System.in);
        File data = new File(scan.nextLine());  
        
        // if user enters illegitimate file path, re-prompt them until file is executable
       while(!(data.exists())){
           System.out.println("File path not executable. Please enter an absolute file path: ");  
           data = new File (scan.nextLine()); 
       }
       
       // create scanner to scan file and count # of rows
       Scanner dS = new Scanner(data); 
       
       //while loop to count # of rows in file
       int numRows = 0;
       while (dS.hasNextLine()){
           numRows++; 
           dS.nextLine(); 
       }
      
    // create array of Quote objects that will contain one object for each line on the file
    Quote[] stockList = new Quote[numRows];
    // create new scanner to scan file, specify that the comma is the delimiter as our file is CSV
    Scanner dataScanner = new Scanner(data);
    dataScanner.useDelimiter(","); 
       
    // use scanner to sift through each line of the file and pull out desired tokens to create Quote objects to be added to stockList 
    for(int i = 0; i < numRows; i++){
        
           //new string that is the next line of the file 
       String dataS = dataScanner.nextLine();
       //new scanner that will read and parse the string we just created usinf commas as delimiter
       Scanner parse = new Scanner(dataS); 
       parse.useDelimiter(",");
       
       // parse out each of our desired tokens and store them as variables 
          String t = parse.next(); 
          int d = parse.nextInt(); 
          double o = parse.nextDouble(); 
          double h = parse.nextDouble(); 
          double l = parse.nextDouble();
          double c = parse.nextDouble();
          int v = parse.nextInt();   
          
       // create new Quote object with variables just created from dataset 
           stockList[i] = new Quote(t,d,o,h,l,c,v);
       }
     
// declare variables to be used for finding dailyGain
    double dailyGain; 
    double x = 0;
    double close; 
    double open; 
    
        // sift through list to find dailyGain for each object in stockList
        for (Quote stockList1 : stockList) {
            close = stockList1.getClose();
            open = stockList1.getOpen();
            dailyGain = close - open;
            // find maximum value of dailyGain by comparing daily gain of stockList[i] to previous dailyGain of stockList[i-1]
            for(int j = 0; j<numRows; j++){
                if(dailyGain > x ){
                    x = dailyGain;
                }
            }}
       // sift through stockList to find the Quote that has biggest dailyGain after the maximum dailyGain has been found 
        for(int k = 0; k <numRows; k++){ 
        if(x == stockList[k].getClose()-stockList[k].getOpen()){
               System.out.println("The biggest Gainer is: "+ stockList[k].getTicker()+", daily gain: "+ (stockList[k].getClose()-stockList[k].getOpen()));   
        }
    }
    
    // declare variables to be used for finding dailyLoss  
    double dailyLoss; 
    double y = 0;
    double cl; 
    double op; 
    
        //sift through data to find most extreme dailyLoss
        for (Quote stockList1 : stockList) {
            cl = stockList1.getClose();
            op = stockList1.getOpen();
            dailyLoss = cl-op;
            // most extreme (most negative) value of dailyLoss
            if(dailyLoss < y ){
                y = dailyLoss;
            }
        }
   
   //sift through stockList to find Quote which had most extreme dailyLoss and print ticker 
     for (int k = 0; k < numRows; k++){
        if(y == (stockList[k].getClose()-stockList[k].getOpen())){
               System.out.println("The biggest Loser is: "+ stockList[k].getTicker()+", daily loss: "+(stockList[k].getClose()-stockList[k].getOpen()));
        }
     }
     
     // find maximum volume 
      int maxVol = 0; 
      for(int i = 0; i < numRows; i++){
          if(stockList[i].getVol() > maxVol){
              maxVol = stockList[i].getVol(); 
          }           
      }
      
     // find which stock had max volume and print ticker 
      for(int i = 0; i < numRows; i++){
          if(stockList[i].getVol() == maxVol){
             String mostActive = stockList[i].getTicker(); 
              System.out.println("The most active stock(s) : " + mostActive+", volume: "+ stockList[i].getVol());
          }
      }
      
      // print out summary statistics with specified format 
        System.out.println("Ticker  Date    Open    High    Low     Close   Volume");
      for(int i = 0; i < 25; i++){
          String t =  stockList[i].getTicker(); 
          int d =  stockList[i].getDate(); 
          double o = stockList[i].getOpen(); 
          double h =  stockList[i].getHigh(); 
          double l = stockList[i].getLow(); 
          double c = stockList[i].getClose(); 
          int v = stockList[i].getVol(); 
          System.out.printf("%s %d  %6.2f  %6.2f  %6.2f  %6.2f  %d\n", t,d,o,h,l,c,v);
        }               
    }
}
        
         

     
       
        
        
    

 

  
    
    
               
           
       
     
       
        
        
    

 

  
    
    

