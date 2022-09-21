/**
 * Data Structures and Algoritms 6th Edition
 * Goodrick, Tamassia, Goldwasser
 * Code Fragment 6.2, The ArrayStack Class
 * A collection of objects that are inserted and removed according to the last-in
 * first-out principle, from an array.This is an array-based implementation of the Stack ADT. 
 * @author Zach Johnson
 * @version 10/8/2021
 */

public class ArrayStack<E> implements Stack<E> {   // class will be generic- can accept any type 
    public static final int CAPACITY = 1000;       // this will be our default capacity
    private E[] data;                              // generic array used for storage
    private int t = -1;                            // index of top element in stack
    public ArrayStack( ){ this(CAPACITY); }        // default constructor 
    public ArrayStack( int capacity ){             // constructor where client specifies array capacity
        data = (E[]) new Object[capacity];         // safe cast of new generic array
    }
    /**
     * Gives current size of Stack 
     * @return int size of current Stack 
     */
    public int size(){                            
        return t+1 ; 
    }
    /**
     * Checks if Stack is empty
     * @return boolean true if Stack is empty 
     */
    public boolean isEmpty(){ return t == -1; }
    /**
     * Pushes a new element on to the top of the Stack 
     * @param e element to be added to the top of the Stack 
     * @throws IllegalStateException if Stack is full 
     */
    public void push( E e ) throws IllegalStateException {
        if (size() == data.length)  // cannot add to ArrayStack if the array is full 
            throw new IllegalStateException("Stack is full, buddy. Try using a linked list.");
       
        data[++t] = e; // increment t before adding new element 
    }
    /**
     * Gets element at top of the Stack 
     * @return element at the top of the Stack 
     */    
    public E top(){
        if( isEmpty())
            return null; 
        return data[t]; 
    }
    /**
     * Removes and returns element at top of Stack 
     * @return element at top of Stack, which was removed
     */
    public E pop(){
        if( isEmpty()) return null; 
        E answer = data[t]; 
        data[t] = null; 
        t--;
        return answer; 
    }
    
    
    
}



