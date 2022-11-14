/**
 *
 * @author Zach Johnson
 */
public class Client {

    /**
     * The method executed on program start
     * @param args 
     */
    public static void main(String[] args) {

        long timeOut = 60000;

        String[] headers = {"N", "Create", "Copy", "Merge",
            "Quick", "Bubble", "eBubble", "Insertion", "Selection", "Radix"};
        long[][] data = new long[4][10];

        // True if not out of memory
        boolean create = true, copy = true;
        // True if those havent timed out yet
        boolean merge = true, quick = true, bubble = true, eBubble = true;
        boolean insertion = true, selection = true, radix = true;

        for (int exp = 3; exp <= 6; exp++) {
            long n = (long) Math.pow(10, exp);
            //System.out.println(n);
            data[exp - 3][0] = n;
            Student[] st = new Student[0];
            Student[] stcopy = new Student[0];

            if (create && copy) {
                try {
                    long createStart = System.currentTimeMillis();
                    st = new Student[(int) n];
                    for (int i = 0; i < st.length; i++) {
                        st[i] = new Student();
                    }
                    data[exp - 3][1] = System.currentTimeMillis() - createStart;
                } catch (OutOfMemoryError oom) {
                    data[exp - 3][1] = -2;
                    create = false;
                    copy = false;
                }
            } else {
                for (int i = 1; i < data[exp - 3].length; i++) {
                    data[exp - 3][i] = -2;
                }
                continue;
            }

            if (copy) {
                try {
                    long copyStart = System.currentTimeMillis();
                    stcopy = new Student[st.length];
                    copyArray(stcopy, st);
                    data[exp - 3][2] = System.currentTimeMillis() - copyStart;
                } catch (OutOfMemoryError oom) {
                    data[exp - 3][2] = -2;
                    copy = false;
                }
            } else {
                for (int i = 1; i < data[exp - 3].length; i++) {
                    data[exp - 3][i] = -2;
                }
                continue;
            }

            // need this otherwise the inital sort is slow,
            // probably because JIT optimizations are being made
            if (exp == 3) {
                try {
                    Sort.mergeSort(stcopy, Student.compareByLName(), timeOut);
                } catch (TimedOutException ex) {
                    data[exp - 3][3] = -1;
                    merge = false;
                }
                copyArray(stcopy, st);
            }

            if (merge) {
                try {
                    long mergeStart = System.currentTimeMillis();
                    Sort.mergeSort(stcopy, Student.compareByLName(), timeOut);
                    data[exp - 3][3] = System.currentTimeMillis() - mergeStart;
                } catch (TimedOutException toe) {
                    data[exp - 3][3] = -1;
                    merge = false;
                }
            } else {
                data[exp - 3][3] = -1;
            }

            if (quick) {
                try {
                    copyArray(stcopy, st);
                    long quickStart = System.currentTimeMillis();
                    Sort.mergeSort(stcopy, Student.compareByStanding(), timeOut);
                    data[exp - 3][4] = System.currentTimeMillis() - quickStart;
                } catch (TimedOutException toe) {
                    data[exp - 3][4] = -1;
                    quick = false;
                }
            } else {
                data[exp - 3][4] = -1;
            }

            if (bubble) {
                try {
                    copyArray(stcopy, st);
                    long bubbleStart = System.currentTimeMillis();
                    Sort.simpleBubbleSort(stcopy, Student.compareById(), timeOut);
                    data[exp - 3][5] = System.currentTimeMillis() - bubbleStart;
                } catch (TimedOutException toe) {
                    data[exp - 3][5] = -1;
                    bubble = false;
                }
            } else {
                data[exp - 3][5] = -1;
            }

            if (eBubble) {
                try {
                    copyArray(stcopy, st);
                    long eBubbleStart = System.currentTimeMillis();
                    Sort.enhancedBubbleSort(stcopy, Student.compareByGPA(), timeOut);
                    data[exp - 3][6] = System.currentTimeMillis() - eBubbleStart;
                } catch (TimedOutException toe) {
                    data[exp - 3][6] = -1;
                    eBubble = false;
                }
            } else {
                data[exp - 3][6] = -1;
            }

            if (insertion) {
                try {
                    copyArray(stcopy, st);
                    long insertionStart = System.currentTimeMillis();
                    Sort.insertionSort(stcopy, Student.compareByFName(), timeOut);
                    data[exp - 3][7] = System.currentTimeMillis() - insertionStart;
                } catch (TimedOutException toe) {
                    data[exp - 3][7] = -1;
                    insertion = false;
                }
            } else {
                data[exp - 3][7] = -1;
            }

            if (selection) {
                try {
                    copyArray(stcopy, st);
                    long selectionStart = System.currentTimeMillis();
                    Sort.selectionSort(stcopy, Student.compareById(), timeOut);
                    data[exp - 3][8] = System.currentTimeMillis() - selectionStart;
                } catch (TimedOutException toe) {
                    data[exp - 3][8] = -1;
                    selection = false;
                }
            } else {
                data[exp - 3][8] = -1;
            }

            if (radix) {
                try {
                    copyArray(stcopy, st);
                    long radixStart = System.currentTimeMillis();
                    Sort.radixSort(stcopy, timeOut, Student.compareByStanding(), Student.compareByGPA(), Student.compareByLName());
                    data[exp - 3][9] = System.currentTimeMillis() - radixStart;
                } catch (TimedOutException toe) {
                    data[exp - 3][9] = -1;
                    radix = false;
                }
            } else {
                data[exp - 3][9] = -1;
            }
        }

        System.out.println(Table.asciiTable("Run time in milliseconds. -1 means sort timed out. -2 means out of memory.", headers, data));
    }

    /**
     * Copy an array from src to dest
     * @param <K>
     * @param dest the destination array
     * @param src the source array
     */
    public static <K> void copyArray(K[] dest, K[] src) {
        for (int i = 0; i < src.length; i++) {
            dest[i] = src[i];
        }
    }
    
}
