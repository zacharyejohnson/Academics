/** SinglyLinkedList Class
 * Code Fragments 3.14, 3.15
 * from
 * Data Structures & Algorithms, 6th edition
 * by Michael T. Goodrich, Roberto Tamassia & Michael H. Goldwasser
 * Wiley 2014
 * Transcribed by
 * @author Zach Johnson     
 * @version 9/21/2021            
 */

public class SinglyLinkedList<E> {
    
    // =============nested node class to describe node structure ===========================
    private static class Node<E> {
       
        private E element; 
        private Node<E> next; 
        
        /**
         * 
         * @param e value of constructed node 
         * @param n value of next node in list 
         */
        public Node( E e, Node<E> n ) {
            element = e; 
            next = n; 
        }
        /**
         * 
         * @return element stored in current node 
         */
        public E getElement() {
            return element; 
        }
        /**
         * 
         * @return Node<E> the next node in the list
         */
        public Node<E> getNext() {
            return next; 
        }
        /**
         * 
         * @param n the value you would like the next node to hold 
         */
        public void setNext( Node<E> n ){
            next = n; 
        }
    }
    //======== instance variables of SinglyLinkedList class ==========================
    
    private Node<E> head = null;  // first node in list; null if list is empty 
    
    private Node<E> tail = null; // last node in list
    
    private int size = 0; // number of nodes in list 
    
    public SinglyLinkedList(){}  // default constructor; creates empty list 
    
//========== access methods =======================================================
    public int size(){    // gets size of the list 
        return size; 
    }
    
    public boolean isEmpty(){   // checks if list has no nodes
        return size == 0; 
    }
    
    public E first(){             // returns first element in list
        if( isEmpty())
            return null; 
        return head.getElement(); 
    }
    
    public E last(){            // returns last element in list 
        if( isEmpty())
                return null; 
        return tail.getElement(); 
    }
// ============ update methods ==============================================
    /**
     * 
     * @param e value of node to be created 
     * adds new node to beginning of list 
     */
    public void addFirst(E e){     // adds element e to head of list 
    
        head = new Node<>( e, head );  
        
        if ( size == 0 )  // check for empty list
            tail = head; 
        
        size++;             // size increases as nodes are made 
        
    }
    /**
     * 
     * @param e value of node to be created 
     * adds new node to the end of the list 
     */
    public void addLast( E e ){
        
        Node<E> newest = new Node<>( e, null ); // node will be the tail so next reference is null 
   
        if( isEmpty())    // checks if list is empty and assiognes head reference to newly created node if it is 
            head = newest; 
        else
            tail.setNext( newest ); 
        
        tail = newest;  // assigns newly created node as the tail 
        
        size++; // increments size as list length has increased 
    }
    /**
     * 
     * @return Node E first node of list 
     * removes and returns first node of list 
     */
    public E removeFirst(){
       
        if( isEmpty() )   // checks if list is empty 
            return null; 
        
        E answer = head.getElement(); // gets current head 
        
        head = head.getNext(); // assigns head reference to node after current head 
        
        size--; // decremenets size since head was removed
        if( size == 0 )  // checks if list is now empty and sets tail to null if it is 
            tail = null;
        
        return answer; // returns value of removed fist node to client 
    }
}
