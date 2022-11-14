/**
 * Data Structures and Algoritms 6th Edition
 * Goodrick, Tamassia, Goldwasser
 * Code Fragment 7.7, Position Interface
 * The Position Interface represents the position ADT
 * @author Zach Johnson (Transcriber)
 * @version 10/17/2021
 */
 public interface Position<E> {
   /**
    * Returns the element stored at this position.
    *
    * @return the stored element
    * @throws IllegalStateException if position no longer valid
    */
   E getElement( ) throws IllegalStateException;
 }
