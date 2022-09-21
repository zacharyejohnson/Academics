/**
 * The generic bag interface holds and provides method signatures for a variety of data
 * @author Zach Johnson
 * @version 9/21/2021
 * @param <E> any object 
 */
public interface Bag<E> {
    /**
     * Gives number of elements in bag 
     * @return int a count of items in the bag
     */
    public int size(); 
    /**
     * Checks if bag is empty 
     * @return true if there are no items in bag 
     */
    public boolean isEmpty(); 
    /**
     * Gives number of times element is in bag 
     * @param e element to be checked for frequency 
     * @return frequency of desired element
     */
    public int getFrequencyOf(E e); 
    /**
     * Checks to see if bag contains element e 
     * @param e element to be checked for containment
     * @return true if element is in bag 
     */
    public boolean contains(E e); 
    /**
     * Adds element to the bag 
     * @param e element to be added 
     */
    public void add(E e); 
    /**
     * Removes element from bag 
     * @param e element to be removed 
     * @return element removed 
     */
    public E remove(E e); 
    /**
     * Removes random element from bag 
     * @return element removed 
     */
    public E remove(); 
    /**
     * Gets value of element at index i 
     * @param i index of list to be retrieved 
     * @return value of element at index i 
     */
    public E get(int i); 
    /**
     * Gives string representation of bag contents 
     * @return contents of bag as string 
     */
    public String toString(); 
    /**
     * Checks to see if an object and bag contents are the same 
     * @param o Object to be compared with bag 
     * @return true if Object and bag contents are the same 
     */
    public boolean equals(Object o); 
    
}
