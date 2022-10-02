/**
 * Data Structures and Algoritms 6th Edition
 * Goodrick, Tamassia, Goldwasser
 * Code Fragment 6.11, LinkedQueue Class
 * A collection of objects that are inserted and removed according to the first-in
 * first-out principle, from a linked list. This uses the SinglyLinkedList FDT
 * to implement the Queue ADT. 
 * @author Zach Johnson (Transcriber)
 * @version 10/8/2021
 */
/** Realization of a FIFO queue as an adaptation of a SinglyLinkedList. */
 public class LinkedQueue<E> implements Queue<E> {
     // constructors 
  private SinglyLinkedList<E> list = new SinglyLinkedList<>( );     // an empty list
  public LinkedQueue( ) { }            // new queue relies on the initially empty list
  
//methods
  /**
   * Get current size of Queue
   * @return int current size of Queue
   */
  public int size( ) { return list.size( ); }
  
  /**
   * Checks if Queue is empty 
   * @return boolean : true if Queue is empty 
   */
  public boolean isEmpty( ) { return list.isEmpty( ); }
  
  /**
   * Adds an element to the back of the Queue
   * @param e element to be added to the back of the Queue
   */
  public void enqueue(E e) { list.addLast(e); }
  
  /**
   * Gets element at the front of the Queue
   * @return e element at the front of the Queue
   */
  public E first( ) { return list.first( ); }
  
  /**
   * Removes and returns element at front of Queue
   * @return e element at front of queue which is removed upon method call
   */
  public E dequeue( ) { return list.removeFirst( ); }
 }