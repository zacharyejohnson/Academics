
import java.util.Random;

/**
 * ArrayBag class is a generic class for constructing arrays of objects
 * @author Zach Johnson
 * @version 9/21/2021
 */
public class ArrayBag<E> implements Bag<E>{
     E[] list;
   int count;
     
    
    /**
     * Scores constructor. The default capacity
     * is 2
     */
    public ArrayBag() {
      list  = (E[]) new Object[2];
    }
    
    /**
     * Scores constructor. If you know before hand about
     * how much capacity you need, use this
     * @param length the initial capacity of the list
     */
    public ArrayBag(int length) {
        list = (E[]) new Object[length];
    }
    
    /**
     * Gives the number of elements in the ArrayBag
     * @return the number of elements in the ArrayBag
     */
    public int size() {
        return count;
    }
    
    /**
     * Returns true if there are no elements in the ArrayBag, and false
 if there are one or more elements in the ArrayBag
     * @return true if there are no elements in the ArrayBag
     */
    public boolean isEmpty() {
        return count == 0;
    }
    
    /**
     * Logically clears the bag
     */
    public void clear() {
        count = 0;
    }
    
    /**
     * Add an element to the ArrayBag
     * @param e the number being added to the end of the ArrayBag
     */
    public void add( E e ) {
        // if the array is not large enough, an array of twice
        // the capacity is created
        if (count + 1 > list.length) {
            E[] temp = (E[]) new Object[list.length * 2];
            for (int i = 0; i < list.length; i++) {  // manual copy 
                 temp[i] =  list[i];
            }
            list = temp;
            temp = null;
        }
        
        // add the element to the array and increment the count
        list[count++] = e;
    }
    
    /**
     * Returns the frequency of a particular number in the ArrayBag
     * @param e the number being tested on
     * @return the number of times  appears in the ArrayBag
     */
    public int getFrequencyOf(E e) {
        int freq = 0;
        for (int i = 0; i < count; i++) {
            if (list[i] == e) {
                freq++;
            }
        }
        
        return freq;
    }
    
    /**
     * checks to see if there is a particular number in the ArrayBag
     * @param e the number being checked
     * @return true if the number is in the bag
     */
    public boolean contains(E e) {
        for (int i = 0; i < count; i++) {
            if (list[i] == e) {
                return true;
            }  
        }
        
        return false;
    }
    
    /**
     * Removes the first occurrence of e in the ArrayBag
     * @param e the number being removed
     */
    public E remove(E e) {
        // find the index of num
        for (int i = 0; i < count; i++) {
            if (list[i] == e) {
                // shift the elements leftward and decrement count
                for (int j = i; j < count - 1; j++) {
                    list[j] = list[j+1];
                }
                count--;
                
            }
        } System.out.println("Element removed: "); 
        return e; 
    } 
    
    /**
     * Remove a random element
     */
    public E remove() {
        Random rand = new Random(count); 
        int index = rand.nextInt(count);
        if(count != 0){
            System.out.println("Element at index "+index+" removed: " + list[index]);
        for (int i = index; i < count - 1; i++) {
            list[i] = list[i+1];
        }
        
    }  count--; 
    return list[index];
    }
    
    /**
     * Finds the element at index i in ArrayBag
     * @param i the index of the array
     * @return element at index i
     * @throws ArrayIndexOutOfBoundsException if the index is outside of the list
     */
    public E get(int i) throws ArrayIndexOutOfBoundsException {
        if (i <= 0 || i > count) {
            System.out.println("invalid index: "+ i);
            throw new ArrayIndexOutOfBoundsException();
        } else {
           return list[i]; 
        }
    }
    
    /**
     * 
     * @return a string representation of ArrayBag
     */
    public String toString() {
        String s = "Scores@count=" + count + ":list=[";
        for (int i = 0; i < count; i++) {
            s += list[i] + (i == count-1 ? "" : ",");
        }
        s += "]";
        return s;
    }
    
    /**
     * 
     * @param o an arbitrary object
     * @return true if the object is a ArrayBag object and has identical content
     */
    public boolean equals(Object o) {
        if (!(o instanceof Object[])) {
            return false;
        }
        ArrayBag s = (ArrayBag) o;
        if (!(count != s.count)) {
            return false;
        }
        for (int i = 0; i < s.count; i++) {
            if (list[i] != s.list[i]) {
                return false;
            }
        }
        return true;
    }
}
