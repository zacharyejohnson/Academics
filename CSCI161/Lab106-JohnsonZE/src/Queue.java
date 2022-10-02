/**
 * Data Structures and Algoritms 6th Edition
 * Goodrick, Tamassia, Goldwasser
 * Code Fragment 6.9, The Queue Interface
 * An ADT interface that describes a collection of objects that are inserted and removed according to the first-in
 * first-out principle. 
 * @author Zach Johnson (Transcriber)
 * @version 10/8/2021
 */
public interface Queue<E> {
   /**
    * Returns the number of elements in the queue.*/
   int size( );
   /** Tests whether the queue is empty. */
   boolean isEmpty( );
   /** Inserts an element at the rear of the queue. */
   void enqueue(E e);
   /** Returns, but does not remove, the first element of the queue (null if empty). */
   E first( );
   /** Removes and returns the first element of the queue (null if empty). */
   E dequeue( );
 }
