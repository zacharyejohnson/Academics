;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname summations) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
;; Data Definition
;; int >= 2
;; example data:
;; int: 3,5,18
;;
;; sum: int -> int
;; input:
;;       n, int >= 2, the n in the sequence 1 to n which will be summed 
;; output:
;;       int, the sum each value in the sequence 1 to n 
(define (sum n)
  (if (< n 2) (error "not a valid input")
  (* n (/ (+ 1 n) 2) )))
;; tests
(check-expect (sum 100) 5050)
(check-expect (sum 8) 36)
(check-expect (sum 11) 66)
