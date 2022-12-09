;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-abbr-reader.ss" "lang")((modname right-max) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
;; Data Definition
;; list of integers 
;; example data:
;; [1,2,3], [-3, -1, 4, 5, 6]
;;
(define l0 empty)
(define l1 (list 4 1 1 1  ))
(define l2 (cons 0 (cons 1 empty)))
(define l3 (cons 0 (cons 1 (cons 2( cons 3 (cons 4 empty))))))
;; right-max: list -> list
;; input:
;;       aloi, list of ints
;; output:
;;       list of ints which are the the max of itself and the elements to the right of it in aloi

(define (right-max aloi)
  [cond
    [(empty? aloi) empty]
    [(empty? (rest aloi)) (first aloi)]
    [(cons? aloi) ( if ( > ( first aloi) (first (right-max (rest aloi))))
                       (cons (first aloi)(right-max(rest aloi)))
                       (cons(first(right-max(rest aloi)))(right-max(rest aloi))))]])
;; tests

(check-expect (right-max l1)  (list 4 1 1 1 ) )
(check-expect (right-max l3)  (list 4 4 4 4 ) )



