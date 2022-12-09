#lang racket
;; Data Definition
;; int >= 3
;; example data:
;; int: 3,5,18
;;
;; sum-angles: int -> num
;; input:
;;       int >=3, number of angles in a polygon
;; output:
;;       num, sum of the degrees in the polygon
(define (sum-angles n)
  (if (< n 3) (error "not a valid int")
  (* 180 (- n 2))))
;; tests
(check-expect (sum-angles 3) 180)
(check-expect (sum-angles 8) 1080)
(check-expect (sum-angles 11) 1620)

  

  




