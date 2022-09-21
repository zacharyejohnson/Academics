
import java.util.Iterator;

/**
 * Tree Interface
 * Code Fragment 8.1
 * from
 * Data Structures & Algorithms, 6th edition
 * by Michael T. Goodrich, Roberto Tamassia & Michael H. Goldwasser
 * Wiley 2014
 * Transcribed by
 * @author Zach Johnson
 */

/** An interface for a tree where nodes can have an arbitrary number of children. */
public interface Tree<E> extends Iterable<E>{
    /**
     * Gets root of the tree 
     * @return position which is the root of tree 
     */
    Position<E> root(); 
    /**
     * Get parents of a given position
     * @param p a position for which you would like to know the parent of 
     * @return the position which is the parent of the inquired node 
     * @throws IllegalArgumentException 
     */
    Position<E> parent(Position<E> p) throws IllegalArgumentException; 
    /**
     * Gives children of given node 
     * @param p parent node
     * @return children of p 
     * @throws IllegalArgumentException 
     */
    Iterable<Position<E>> children(Position<E> p) throws IllegalArgumentException; 
    /**
     * Gives number of children 
     * @param p parent node
     * @return number of children p has 
     * @throws IllegalArgumentException 
     */
    int numChildren(Position<E> p) throws IllegalArgumentException; 
    /**
     * Tells whether position is internal 
     * @param p position
     * @return true if position is internal
     * @throws IllegalArgumentException
     * */
    boolean isInternal(Position<E> p) throws IllegalArgumentException; 
    /**
     * Tels whether position is external 
     * @param p position
     * @return true if position is external 
     * @throws IllegalArgumentException 
     */
    boolean isExternal(Position<E> p) throws IllegalArgumentException; 
    /**
     * Tells whether position is root of tree 
     * @param p position to be analyzed 
     * @return true if position is root of tree 
     * @throws IllegalArgumentException 
     */
    boolean isRoot(Position<E> p) throws IllegalArgumentException; 
    /**
     * Gets size of tree 
     * @return int number of positions on tree 
     */
    int size(); 
    /**
     * Tells whether tree is empty
     * @return true if tree has no positions
     */
    boolean isEmpty(); 
   
    Iterator<E> iterator(); 
    Iterable<Position<E>> position();
}
