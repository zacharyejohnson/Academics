/**
 * Data Structures and Algoritms 6th Edition
 * Goodrick, Tamassia, Goldwasser
 * Code Fragment 6.10, ArrayQueue Class
 * A collection of objects that are inserted and removed according to the first-in
 * first-out principle, from an array. This is an array-based implementation of the Queue ADT. 
 * @author Zach Johnson (Transcriber)
 * @version 10/8/2021
 */

/** Implementation of the queue ADT using a fixed-length array. */
public class ArrayQueue<E> implements Queue<E> {
 // instance variables
  public static final int CAPACITY = 0; 
  private E[ ] data;                    // generic array used for storage
  private int f = 0;                    // index of the front element
  private int sz = 0;                   // current number of elements

  // constructors
  public ArrayQueue( ) {this(CAPACITY);} // constructs queue with default capacity
  public ArrayQueue(int capacity) {     // constructs queue with given capacity
    data = (E[ ]) new Object[capacity]; // safe cast; compiler may give warning
  }

  // methods
  /**
   * Returns the number of elements in the queue. 
   * @return int size of the Queue
   */
  public int size( ) { return sz; }

  /**
   * Tests whether the queue is empty.
   * @return boolean : true if Queue is empty
   */
  public boolean isEmpty( ) { return (sz == 0); }

  /**
   * Inserts an element at the rear of the queue.
   * @param e element to be inserted at the back of the Queue
   * @throws IllegalStateException cannot add new elements to Queue if Queue is full
   */
  public void enqueue(E e) throws IllegalStateException {
    if (sz == data.length) throw new IllegalStateException("Queue is full");
    int avail = (f + sz) % data.length;  // use modular arithmetic
    data[avail] = e;
    sz++;
  }

  /** 
   * Returns, but does not remove, the first element of the queue (null if empty). 
   * @return e first element in the Queue
   */
  public E first( ) {
    if (isEmpty( )) return null;
    return data[f];
  }

  /** 
   * Removes and returns the first element of the queue (null if empty).
   * @return element at front of Queue which was removed 
   */
  public E dequeue( ) {
    if (isEmpty( )) return null;
    E answer = data[f];
    data[f] = null;                      // dereference to help garbage collection
    f = (f + 1) % data.length;
    sz--;
    return answer;
  }
}
