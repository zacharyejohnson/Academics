/**
 * SinglyLinkedList Class
 * Code Fragments 3.14, 3.15
 * from
 * Data Structures & Algorithms, 6th edition
 * by Michael T. Goodrich, Roberto Tamassia & Michael H. Goldwasser
 * Wiley 2014
 * Transcribed by
 * @author Zach Johnson
 */
public class SinglyLinkedList<E>{
        //=========== nested node class=========//
        private static class Node<E>{
            private E element;    // reference to the element stored at this node 
            private Node<E> next; // reference to the next node in the list
            public Node(E e, Node<E> n){
                element = e; 
                next = n; 
            }
            public E getElement(){
                return element; 
            }
            public Node<E> getNext(){
                return next; 
            }
            public void setNext(Node<E> n){
                next = n; 
            }  
        }//====== End of nested node class=========//   
        
        // Instance variables of the SinglyLinkedList Class
        private Node<E> head = null;  // first node in list-null if empty
        private Node<E> tail = null;  // last node in list 
        private int size = 0;         // number of nodes in list 
        // constructs an initially empty list 
        public SinglyLinkedList(){}
        // access methods
        public int size(){
            return size; 
        }
        public boolean isEmpty(){
            return size == 0; 
        }
        public E first(){
            if( isEmpty() ) return null; 
            return head.getElement();
        }
        public E last(){
            if( isEmpty()) return null; 
            return tail.getElement(); 
        }
        // update methods 
        public void addFirst( E e ){  // adds element e to the front of the list
            head = new Node<>(e, head); // create and link a new node 
            if( isEmpty())
                tail = head; // special case: new node becomes tail also
            size++; 
            
        }
        public void addLast( E e ){
            Node<E> newest = new Node<>(e, null);
            if( isEmpty() )
                head = newest; // special case : previously empty list 
            else
                tail.setNext(newest); 
            tail = newest; 
            size++; 
        }
        /**
         * Removes and returns first element 
         * @return E element contained at first node
         */
        public E removeFirst(){
            if( isEmpty() )
                return null; // nothing to remove
            E answer = head.getElement(); 
            head = head.getNext(); 
            size--; 
            if( size == 0 )
                tail = null; // specila case as tail is now empty 
            return answer; 
        }
        /**
         * The toString method returns a String representation of our class 
         * @return  a String representation of the SinglyLinkedList class 
         */
        public String toString(){
            String s = getClass().getName() + "@" + "size" + ":list = ["; 
            Node<E> p = head; 
            do{
                s += p.getElement().toString(); 
                if( p != tail ){
                    s += ",";
                }
                p = p.next; 
            } while( p != head);
            s += "]"; 
            return s; 
        }
        /**
     * 
     * @param o any object
     * @return true if o has identical content
     */
    public boolean equals(Object o) {
        if (!(o instanceof SinglyLinkedList)) {
            return false;
        }
        SinglyLinkedList<E> s = (SinglyLinkedList<E>) o;
        if (size != s.size) {
            return false;
        }
        Node<E> p = head;
        Node<E> q = s.head;
        do {
            if (!p.getElement().equals(q.getElement())) {
                return false;
            }
            p = p.next;
            q = q.next;
        } while (p != head);
        
        return false;
    }
}
