/**
 * Data Structures and Algoritms 6th Edition
 * Goodrick, Tamassia, Goldwasser
 * Code Fragment 6.2, The ArrayStack Class
 * A collection of objects that are inserted and removed according to the last-in
 * first-out principle; The LinkedStack Class uses the SinglyLinkedList FDT 
 * to implement the Stack ADT
 * @author Zach Johnson(Transcriber)
 * @version 10/8/2021
 */
public class LinkedStack<E> implements Stack<E> {
   
  private SinglyLinkedList<E> list = new SinglyLinkedList<>( );    // an empty list
 
  
  public LinkedStack( ) { }            // default constructor - new stack relies on the initially empty list
  
  /**
   * Gets current size of the Stack 
   * @return int size of the stack( number of elements in the stack )
   */
  public int size( ) { return list.size( ); }
  
  /**
   * Checks if the Stack is empty - relies on list methods from SinglLinkedList class 
   * @return boolean : true if the Stack has no elements
   */
  public boolean isEmpty( ) { return list.isEmpty( ); }
  
  /**
   * adds an element to the front of the Stack
   * @param e element to be added to front of Stack 
   */
  public void push(E e) { list.addFirst(e); }
  
  /**
   * Gets and returns element at top of Stack
   * @return e element at the top of the Stack 
   */
  public E top( ){
      return list.first( );
  }
  
  /**
   * Removes and returns element at top of Stack 
   * @return e element at top of stack which was removed 
   */
  public E pop( ) { return list.removeFirst( ); }
 
  public boolean equals(Object o) {
        if (!(o instanceof LinkedStack)) {
            return false;
        }
        LinkedStack<E> s = (LinkedStack<E>) o;
        if(!o.equals(s)) {
            return false;
        }
   if(s.top() == null){
       return false; 
   }
        else{
            return true;
        }
    }
}

  