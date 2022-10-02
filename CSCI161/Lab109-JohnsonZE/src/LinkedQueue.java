/**
 * LinkedQueue Class
 * Code Fragment 6.11
 * from
 * Data Structures & Algorithms, 6th edition
 * by Michael T. Goodrich, Roberto Tamassia & Michael H. Goldwasser
 * Wiley 2014
 * Transcribed by
 * @author Zach Johnson
 */
public class LinkedQueue<E> implements Queue<E> {
    private SinglyLinkedList<E> list = new SinglyLinkedList<>(); 
    public LinkedQueue( ) {} // creates new empty queue
    
    public int size(){
        return list.size(); 
    }
   
    public boolean isEmpty(){
        return list.isEmpty(); 
    }
    
    public void enqueue( E e){
        list.addLast(e);
    }
    public E first(){
        return list.first(); 
    }
    
    public E dequeue(){
        return list.removeFirst(); 
    }
}
