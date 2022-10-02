/**
 * A Client testing out the BinaryTree and it's traversals
 * @author Zach Johnson
 * @version 10/21/2021
 */
public class Client {
    /**
     * 
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        
        LinkedBinaryTree<String> expr = new LinkedBinaryTree<>();
        // a is the root of the tree
        Position a, b, c, d, e, f, g, h, i;
        a = expr.addRoot("+");
        b = expr.addLeft(a, "+");
        c = expr.addLeft(b, "2");
        expr.addRight(b, "9");
       d = expr.addRight(a, "-");
       e = expr.addRight(d, "*");
       f = expr.addLeft(e, "3");
       g = expr.addRight(e, "8"); 
       h = expr.addLeft(d, "7"); 
       
  System.out.println("The original expression:");
       System.out.println("2+9 +(7-(3*8))\n");
        
        System.out.println("Preorder traversal:");
        Iterable<Position<String>> preIter = expr.preorder();
        for (Position<String> s : preIter) {
            System.out.print(s.getElement() + " ");
        }
        System.out.println("\n");
        
        System.out.println("Inorder traversal:");
        Iterable<Position<String>> inIter = expr.inorder();
        for (Position<String> s : inIter) {
            System.out.print(s.getElement() + " ");
        }
        System.out.println("\n");
        
        System.out.println("Postorder traversal:");
        Iterable<Position<String>> postIter = expr.postorder();
        for (Position<String> s : postIter) {
            System.out.print(s.getElement() + " ");
        }
        System.out.println("\n");
        
        System.out.println("Breadth traversal:");
        Iterable<Position<String>> breadthIter = expr.breadthfirst();
        for (Position<String> s : breadthIter) {
            System.out.print(s.getElement() + " ");
        }
        System.out.println("\n");
        
        System.out.println("Parenthesized representation:");        
        printParenthesize(expr, a);
        System.out.println();
    }
    
    /**
     * print a parenthesized representation of the tree. Suited for arithmetic trees.
     * @param <E>
     * @param T the tree you want to print
     * @param p the node which you want to print from
     */
    public static <E> void printParenthesize(LinkedBinaryTree<E> T, Position<E> p) {
        if (T.left(p) != null) {
            System.out.print("(");
            printParenthesize(T, T.left(p));
        }
        System.out.print(p.getElement());
        if (T.right(p) != null) {
            printParenthesize(T, T.right(p));
            System.out.print(")");            
        }
    }
}