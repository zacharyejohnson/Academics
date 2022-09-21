
import java.util.Random;

/**
 * The LinkedBag class  implements the Generic Bag Interface created earlier.  
 * This class will include a generic type Parameter as part of class declaration. 
 * When a client class uses the LinkedBag the client will specify the actual type 
 * @author Zach Johnson
 * @version 9/24/2021
 */
public class LinkedBag<E> implements Bag<E> {
    
   private SinglyLinkedList<E> list; 
    private int count; 
    
    public LinkedBag(){
        list = new SinglyLinkedList<E>(); 
    }
    
    public LinkedBag( int capacity ){
        list = new SinglyLinkedList<E>(); 
    }
    /**
     * Returns size of the linked bag 
     * @return int size of the linked bag 
     */
    public int size(){
        return count; 
    }
    /**
     * Checks if bag is empty 
     * @return true if there are no items in bag 
     */
    public boolean isEmpty(){
        return count == 0;
    }
    /**
     * Gives number of times element is in bag 
     * @param e element to be checked for frequency 
     * @return frequency of desired element
     */
    public int getFrequencyOf(E e){
        int freq = 0;
        for (int i = 0; i < count; i++) {
            if (list.first().equals(e)) {
                freq++;
            }
            list.addLast(list.removeFirst());
        }
        return freq;
    }
    /**
     * Checks to see if bag contains element e 
     * @param e element to be checked for containment
     * @return true if element is in bag 
     */
    public boolean contains(E e){
        boolean inBag = false; 
        for (int i = 0; i < count; i++) {
           // if !inBag is true, than we don't need to check .equals()
            if (!inBag && list.first().equals(e)) {
                inBag = true;
            }
            list.addLast(list.removeFirst());
        }

        return inBag;
    }
            ; 
    /**
     * Adds element to the bag 
     * @param e element to be added 
     */
    public void add(E e){
        list.addFirst(e);
        count++; 
    }
    /**
     * Removes element from bag 
     * @param e element to be removed 
     * @return element removed 
     */
    public E remove(E e){
             boolean isRemoved = false;
        for (int i = 0; i < count; i++) {
            // !isRemoved is present so that only one is removed
            // it is also there so the .equals() methoed is not
            // called unessarly
            if (!isRemoved && list.first().equals(e)) {
                list.removeFirst();
                count--;
                isRemoved = true;
            } else {
                list.addLast(list.removeFirst());
            }
        }
        
        return e;
    }
    /**
     * Removes random element from bag 
     * @return element removed 
     */
    public E remove(){
        Random rand = new Random();
        int index = rand.nextInt(count);
        
        E element = null;
        for (int i = 0; i < count; i++) {
            if (i == index) {
                element = list.removeFirst(); 
            } else {
                list.addLast(list.removeFirst());   
            }
        } 
        count--;
        
        return element;
    }
    /**
     * Gets value of element at index i 
     * @param i index of list to be retrieved 
     * @return value of element at index i 
     */
    public E get(int i){
         // if the method is called with an invalid index
        if (i < 0 || i >= count) {
            throw new ArrayIndexOutOfBoundsException();
        }
        
        E element = null;
        for (int j = 0; j < count; j++) {
            if (j == i) {
                element = list.first();
            }
            list.addLast(list.removeFirst());
        }
        return element;
    }
    /**
     * Gives string representation of bag contents 
     * @return contents of bag as string 
     */
    public String toString(){
        String s = getClass().getName() + "@" 
                + "count=" + count + ":elements=[";
        for (int i = 0; i < count; i++) {
            s += list.first();
            // we don't want a comma after the last element
            if (i != count - 1) {
                s += ",";
            }
            list.addLast(list.removeFirst());
        }

        s += "]";
        return s;
    } 
    /**
     * Checks to see if an object and bag contents are the same 
     * @param o Object to be compared with bag 
     * @return true if Object and bag contents are the same 
     */
    public boolean equals(Object o){
        if (!(o instanceof LinkedBag)) {
            return false;
        }
        LinkedBag<E> l = (LinkedBag<E>) o;
        if (count != l.count) {
            return false;
        }
        boolean equal = true;

        for (int i = 0; i < count; i++) {
            if (equal && !(list.first().equals(l.list.first()))) {
                equal = false;
            }
            list.addLast(list.removeFirst());
            l.list.addLast(l.list.removeFirst());
        }
        return equal;
    } 
    
}

