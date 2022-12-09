;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-abbr-reader.ss" "lang")((modname odds-only) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
;; Data Definition
;; list of integers 
;; example data:
;; [1,2,3], [-3, -1, 4, 5, 6]
;;
(define l0 empty)
(define l1 (cons 1 empty))
(define l2 (cons 0 (cons 1 empty)))
(define l3 (cons 0 (cons 1 (cons 2( cons 3 (cons 4 empty))))))

;; odds-only: list -> list
;; input:
;;       aloi, list of ints
;; output:
;;       list of ints which were odd from aloi
(define (odds-only aloi)
  (cond
    [(empty? aloi) empty]
    [(cons? aloi) ( if ( odd? (first aloi))
                       (cons (first aloi)(odds-only (rest aloi)))
                       (odds-only (rest aloi)))]))
  
;; tests
(check-expect (odds-only l2)  (list 1) )
(check-expect (odds-only l3)  (list 1 3) )