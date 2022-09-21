/**
 * Queue interface
 * Code Fragment 6.9
 * from
 * Data Structures & Algorithms, 6th edition
 * by Michael T. Goodrich, Roberto Tamassia & Michael H. Goldwasser
 * Wiley 2014
 * Transcribed by
 * @author Zach Johnson
 */
public interface Queue<E> {
    /** 
     * Returns the number of elements in the queue. 
     * @return int size of Queue 
     */
    int size();
    /** 
     * Tests whether the queue is empty
     * @return true if Queue is empty 
     */
    boolean isEmpty();
    /** 
     * Inserts an element at the rear of the queue. 
     * @param e element to be inserted 
     */
    void enqueue(E e);
    /** 
     * Returns, but does not remove, the first element of the queue (null if empty).
     * @return e first element in the Queue 
     */
    E first();
    /** 
     * Removes and returns the first element of the queue (null if empty).
     * @return e element at beginning of list which was removed 
     */
    E dequeue();
}