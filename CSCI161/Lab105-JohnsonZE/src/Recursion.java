
import java.io.File;
import java.io.FileNotFoundException;

/**
 * The Recursion Class implements two recursive methods 
 * @author Zach Johnson
 * @version 9/28/2021
 */
public class Recursion{
    /**
     * Computes the nth harmonic number 
     * @param n n-th degree of the harmonic sequence
     * @return nth degree harmonic of harmonic sequence 
     */
    public static double harmonic( int n ){
       // check if user passed an invalid integer 
        if ( n < 1 )
            System.out.println("Invalid integer. Must be greater >= 1. Try again, respectfully");
        if ( n == 1 )
            return 1; 
        else 
            return ( 1.0 / n ) + harmonic( n-1 ); 
        
    }
    
  
    /**
     * Implements isabels technique for summing the values in an array whose length is a power of two
     * @param a an int array of length n, n MUST be a power of two 
     * @return the sum of the values of the array 
     */
    public static int isabelsTechnique( int[] a ) throws IllegalArgumentException{
         // if a.length is a power of 2, then there should only be one one-bit
        if (Integer.bitCount(a.length) != 1){ 
            throw new IllegalArgumentException("isabelsTechnique(int[] a) requires a.length to be a power of 2");
        }
        if ( a.length == 1)
            return a[0]; 
        int[] b = new int[a.length / 2]; 
        for (int i = 0; i < b.length-1; i++) {
            b[i] = a[2*i]+a[2*i+1]; 
        }   
        return isabelsTechnique( b ); 
        
        
    }
    /**
     * find command
     * @param targetFilename the file trying to be found
     * @param startPath the path we are looking in
     * @throws java.io.FileNotFoundException
     */
    public static void findFile(String targetFilename, String startPath) throws FileNotFoundException {
        File dir = new File(startPath);
        File f = new File(startPath, targetFilename);
        // if the file is found
        if (f.exists()) {
            System.out.println(f.getAbsolutePath());
        } else { throw new FileNotFoundException("Not a valid file"); }
        if (dir.isDirectory()) {
            File[] subdirs = dir.listFiles();
            for (int i = 0; i < subdirs.length; i++) {
                // if the directory is unreaderable, then a NullPointerException
                // will be thrown
                if (subdirs[i].canRead() && subdirs[i].isDirectory()) {
                    findFile(targetFilename, subdirs[i].getAbsolutePath());
                }
            }
        }
    }
}
