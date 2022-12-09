;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname my-positive) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
;; Data Definition
;; num, int or float 
;; example data:
;; -10, -2.2, 0, 1, 3.14, 25
;;
;; my-positive?: num -> boolean
;; input:
;;       n, num, to be analyzed for positivity
;; output:
;;       boolean, indicating whether n is positive, "ambiguous" if n = 0
(define (my-positive? n)
  (cond
    [(< n 0) false]
    [(= n 0) "ambiguous"]
    [(> n 0) true])
  )
;; tests
(check-expect (my-positive? -2) false)
(check-expect (my-positive? -8.35) false)
(check-expect (my-positive? 0) "ambiguous")
(check-expect (my-positive? 3.14) true)
(check-expect (my-positive? 420) true)