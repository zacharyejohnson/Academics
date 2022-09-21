
import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.InputMismatchException;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JOptionPane;


/**
 * Recursion and user interface in the Client class
 * @author Zach Johnson
 * @version 10/1/2021
 */
public class Client {

    /**
     * Ran at start
     * @param args the command line arguments
     */
    public static void main(String[] args) throws FileNotFoundException {
        prompt();
    }
    
    /**
     * The main prompt for the user
     */
    private static void prompt() throws FileNotFoundException {
        String[] options = {"Harmonic","Isabel's Algorithim","Find File","Cancel"};
        int i = JOptionPane.showOptionDialog(null, "Which algorithim would you like to test?", 
                "Lab105", JOptionPane.DEFAULT_OPTION, JOptionPane.QUESTION_MESSAGE, 
                null, options, null);
        
        if (i == 0) {
            harmonicPrompt();
        } else if (i == 1) {
            isabelPrompt();
        } else if (i == 2) {
            findPrompt();
        } else if (i == 3) {
            return;
        }
    }
    
    /**
     * Prompt for the user to calculate the nth harmonic
     */
    private static void harmonicPrompt() {
        String input = JOptionPane.showInputDialog(null, "Calculate the nth harmonic", "Lab105", JOptionPane.DEFAULT_OPTION);
        // if they hit cancel
        if (input == null) {
            try {
                prompt();
            } catch (FileNotFoundException ex) {
                Logger.getLogger(Client.class.getName()).log(Level.SEVERE, null, ex);
            }
            return;
        }
        // loop while input is invalid
        while (!input.matches("\\d+") || Integer.parseInt(input) < 0) {
            System.out.println("nthHarmonic: Invalid input for harmonic (" +input + "), n should be greater than 0");
            input = JOptionPane.showInputDialog(null, "Invalid input, enter n > 0", "Lab105", JOptionPane.DEFAULT_OPTION);
            // if the hit cancel
            if (input == null) {
                try {
                    prompt();
                } catch (FileNotFoundException ex) {
                    Logger.getLogger(Client.class.getName()).log(Level.SEVERE, null, ex);
                }
                return;
            }
        }
        int n = Integer.parseInt(input);
        double h = Recursion.harmonic(n);
        System.out.println("nthHarmonic: nthHarmonic(" + n + ") = " + h);
        JOptionPane.showMessageDialog(null, "Harmonic " + n + " is " + h, "Lab105", JOptionPane.INFORMATION_MESSAGE);
        try {
            prompt();
        } catch (FileNotFoundException ex) {
            Logger.getLogger(Client.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
    /**
     * Prompt to calculate the sum of a file using isabelSum
     */
    private static void isabelPrompt() {
        String inputFile = JOptionPane.showInputDialog(null, "Enter a file", "Lab105", JOptionPane.DEFAULT_OPTION);
        // if the user hits cancel
        if (inputFile == null) {
            try {
                prompt();
            } catch (FileNotFoundException ex) {
                Logger.getLogger(Client.class.getName()).log(Level.SEVERE, null, ex);
            }
            return;
        }
        
        File f = new File(inputFile);
        int[] array = fileChecker(f);
        // loop while file is a directory, doesn't exist, or is invalid
        while (array == null) {
            if (!f.exists() || f.isDirectory()) {
                System.out.println("isabelSum: User tried Isabel's algorithem on non-existent file " + inputFile);                
                inputFile = JOptionPane.showInputDialog(null, "File not found, enter a different file", "Lab105", JOptionPane.DEFAULT_OPTION);
            } else {
                System.out.println("isabelSum: Unable to use Isabel's algorithem on " + inputFile);
                inputFile = JOptionPane.showInputDialog(null, "Unable to use Isabel's algorithm, enter a different file", "Lab105", JOptionPane.DEFAULT_OPTION);
            }
            if (inputFile == null) {
                try {
                    // if the user hits cancel
                    prompt();
                } catch (FileNotFoundException ex) {
                    Logger.getLogger(Client.class.getName()).log(Level.SEVERE, null, ex);
                }
                return;
            }
            f = new File(inputFile);
            array = fileChecker(f);
        }
        int sum = Recursion.isabelsTechnique(array);
        System.out.println("isabelSum: The sum of " + inputFile + " is " + sum);
        JOptionPane.showMessageDialog(null, "The sum is " + sum, "Lab105", JOptionPane.INFORMATION_MESSAGE);
        try {
            prompt();
        } catch (FileNotFoundException ex) {
            Logger.getLogger(Client.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
    /**
     * Helper method for isabelPrompt()
     * @param f the file being summed
     * @return the array of integers within the file, or null if the
     *      file is not found or doesn't have 2^n number of numbers
     */
    private static int[] fileChecker(File f) {
        try {
            Scanner scan = new Scanner(f);
            ArrayBag<Integer> numbers = new ArrayBag<Integer>();
            System.out.println("isabelSum: Reading " + f.getAbsolutePath());
            // fetching the numbers from the file
            while (scan.hasNext()) {
                try {
                    int i = scan.nextInt();
                    System.out.println(i);
                    numbers.add(i);
                } catch (InputMismatchException ime) {
                    scan.next();
                }
            }
            // if the number of numbers is not a power of 2
            if (Integer.bitCount(numbers.size()) != 1) {
                return null;
            }
            // copying the numbers from ArrayBag to primative int array
            int[] array = new int[numbers.size()];
            for (int i = 0; i < numbers.size(); i++) {
                 array[i] = numbers.get(i);
            }

            return array;
        }
        catch (FileNotFoundException fnfe)
        {
            return null;
        }
        
    }
    
    /**
     * Prompt for the user to use find
     */
    private static void findPrompt() throws FileNotFoundException {
        String inputPath = JOptionPane.showInputDialog(null,"Enter a path", "Lab105", JOptionPane.DEFAULT_OPTION);
        // if the user hits cancel
        if (inputPath == null) {
            prompt();
            return;
        }
        File f = new File(inputPath);
        
        while (!f.isDirectory()) {
            System.out.println("find: path " + inputPath + " not found");
            inputPath = JOptionPane.showInputDialog(null,"Path not found, enter a path", "Lab105", JOptionPane.DEFAULT_OPTION);
            f = new File(inputPath);
        }
        
        String inputFilename = JOptionPane.showInputDialog(null,"Enter a filename", "Lab105", JOptionPane.DEFAULT_OPTION);
        // if the user hits cancel
        if (inputFilename == null) {
            prompt();
            return;
        }
        System.out.println("find: finding " + inputFilename + " in " + inputPath);
        Recursion.findFile(inputFilename, inputPath);
        JOptionPane.showMessageDialog(null, "Output shown in the console");
        prompt();
    }
}
