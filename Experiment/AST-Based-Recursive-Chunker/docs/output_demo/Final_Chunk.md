```lisp 
Final chunk: ; This cond is not a part of a chapter 2.1 but I wanted to implement this for further usage.
Chunk size: 92
-----------------------------------------------------------
Final chunk: (= (cond $com_list)
    (if (== $com_list ())
        (empty)
        (case (car-atom $com_list)
        (
            ((Else $res) $res)
            (($cond $res) (if $cond $res (cond (cdr-atom $com_list))))
        ) )))
Chunk size: 222
-----------------------------------------------------------
Final chunk: (: Else (-> Atom Atom))
Chunk size: 23
-----------------------------------------------------------
Final chunk: (= (sub-rat $x $y)
  (make-rat (- (* (numer $x) (denom $y))
               (* (numer $y) (denom $x)))
            (* (denom $x) (denom $y))))
Chunk size: 141
-----------------------------------------------------------
Final chunk: (= (fib $n)
    (if (== $n 0)
        0
        (if (== $n 1)
            1
            (+ (fib (- $n 1)) (fib (- $n 2))))))
Chunk size: 124
-----------------------------------------------------------
Final chunk: ; Currently metta has no cond so I've decided to write it myself. Thanks to Vitaly Bogdanov, i was able to.
Chunk size: 107
-----------------------------------------------------------
Final chunk: ; Though regular fib is much faster so cond won't be used further unfortunately.
Chunk size: 80
-----------------------------------------------------------
Final chunk: (= (fib_cond $n)
    (cond
    (
        ((== $n 0) 0)
        ((== $n 1) 1)
        (Else (+ (fib_cond (- $n 1)) (fib_cond (- $n 2))))
    )))
!(assertEqual
    (fib_cond 5)
    (fib 5))
(: fib_cond (-> Number Number))
Chunk size: 219
-----------------------------------------------------------
Final chunk: (= (make-pair $x $y) ($x . $y))
Chunk size: 31
-----------------------------------------------------------
Final chunk: (= (first-pair $x) (let ($a . $b) $x $a))
Chunk size: 41
-----------------------------------------------------------
Final chunk: (= (second-pair $x) (let ($a . $b) $x $b))
Chunk size: 42
-----------------------------------------------------------
Final chunk: (= (make-rat $x $y) (make-pair $x $y))
Chunk size: 38
-----------------------------------------------------------
Final chunk: (= (add-rat $x $y)
  (make-rat (+ (* (numer $x) (denom $y))
               (* (numer $y) (denom $x)))
            (* (denom $x) (denom $y))))
Chunk size: 141
-----------------------------------------------------------
Final chunk: (= (mul-rat $x $y)
  (make-rat (* (numer $x) (numer $y))
            (* (denom $x) (denom $y))))
Chunk size: 96
-----------------------------------------------------------
Final chunk: (= (div-rat $x $y)
  (make-rat (* (numer $x) (denom $y))
            (* (denom $x) (numer $y))))
Chunk size: 96
-----------------------------------------------------------
Final chunk: (= (equal-rat? $x $y)
  (= (* (numer $x) (denom $y))
     (* (numer $y) (denom $x))))
Chunk size: 85
-----------------------------------------------------------
Final chunk: ; get-rat func is introduced to use assertEqual instead of print-rat.
Chunk size: 69
-----------------------------------------------------------
Final chunk: (= (print-rat $x)
    (println! (get-rat $x)))
Chunk size: 46
-----------------------------------------------------------
Final chunk: (= (one-half) (make-rat 1 2))
Chunk size: 29
-----------------------------------------------------------
Final chunk: (= (numer $x) (let ($a . $b) $x $a))
Chunk size: 36
-----------------------------------------------------------
Final chunk: (= (denom $x)
    (let ($a . $b) $x $b))
Chunk size: 40
-----------------------------------------------------------
Final chunk: ; This line should print [(1 / 2)]
Chunk size: 34
-----------------------------------------------------------
Final chunk: ;!(print-rat (make-rat 1 2))
Chunk size: 28
-----------------------------------------------------------
Final chunk: (= (y-point $pt) (second-pair $pt))
Chunk size: 35
-----------------------------------------------------------
Final chunk: (= (one-third) (make-rat 1 3))
Chunk size: 30
-----------------------------------------------------------
Final chunk: (= (make-point $x $y) (make-pair $x $y))
!(assertEqual
    (make-point 5 2)
    (5 . 2))
Chunk size: 88
-----------------------------------------------------------
Final chunk: (= (make-segment $start $end) (make-pair $start $end))
!(assertEqual
    (make-segment (make-point 1 2) (make-point 5 7))
    ((1 . 2) . (5 . 7)))
Chunk size: 146
-----------------------------------------------------------
Final chunk: (= (remainder $x $y) (% $x $y))
Chunk size: 31
-----------------------------------------------------------
Final chunk: (= (gcd $a $b)
    (if (== $b 0)
        $a
        (gcd $b (remainder $a $b))))
Chunk size: 80
-----------------------------------------------------------
Final chunk: (= (make-rat2 $n $d)
    (let $g (gcd $n $d)
        (make-pair (/ $n $g) (/ $d $g))))
Chunk size: 86
-----------------------------------------------------------
Final chunk: (= (add-rat2 $x $y)
  (make-rat2 (+ (* (numer $x) (denom $y))
               (* (numer $y) (denom $x)))
            (* (denom $x) (denom $y))))
Chunk size: 143
-----------------------------------------------------------
Final chunk: (= (midpoint-segment $seg)
    (let*
    (
        ($xs (x-point (start-segment $seg)))
        ($ys (y-point (start-segment $seg)))
        ($xe (x-point (end-segment $seg)))
        ($ye (y-point (end-segment $seg)))
    )
    (make-point (/ (+ $xs $xe) 2.0) (/ (+ $ys $ye) 2.0))))
!(assertEqual
    (midpoint-segment (make-segment (make-point 1 2) (make-point 5 7)))
    (3.0 . 4.5))
Chunk size: 386
-----------------------------------------------------------
Final chunk: ; Exercise 2.1.
Chunk size: 15
-----------------------------------------------------------
Final chunk: ;
Chunk size: 1
-----------------------------------------------------------
Final chunk: ; Define a better version of make-rat that handles both positive and negative arguments.
Chunk size: 88
-----------------------------------------------------------
Final chunk: ; make-rat should normalize the sign so that if the rational number is positive, both the numerator and
Chunk size: 103
-----------------------------------------------------------
Final chunk: ; denominator are positive, and if the rational number is negative, only the numerator is negative.
Chunk size: 99
-----------------------------------------------------------
Final chunk: (= (Abs $x) (if (< $x 0) (* $x -1) $x))
Chunk size: 39
-----------------------------------------------------------
Final chunk: (= (better_make-rat $n $d)
    (let $g (gcd $n $d)
        (if (> (* $n $d) 0)
            (make-pair (/ $n $g) (/ $d $g))
            (make-pair (* -1.0 (Abs (/ $n $g))) (Abs (/ $d $g))))))
Chunk size: 190
-----------------------------------------------------------
Final chunk: ; Same as get-rat
Chunk size: 17
-----------------------------------------------------------
Final chunk: (= (print-point $p)
    (println! (get-point $p)))
Chunk size: 50
-----------------------------------------------------------
Final chunk: (= (get-rat $x)
    ((numer $x)/(denom $x)))
!(assertEqual
    (get-rat (make-rat 1 2))
    (1 / 2))
!(assertEqual
    (get-rat (add-rat (one-half) (one-third)))
    (5 / 6))
!(assertEqual
    (get-rat (mul-rat (one-half) (one-third)))
    (1 / 6))
!(assertEqual
    (get-rat (add-rat (one-third) (one-third)))
    (6 / 9))
!(assertEqual
    (get-rat (add-rat2 (one-third) (one-third)))
    (2.0 / 3.0))
!(assertEqual
    (get-rat (better_make-rat 1.0 2.0))
    (1.0 / 2.0))
Chunk size: 474
-----------------------------------------------------------
Final chunk: !(assertEqual
    (get-rat (better_make-rat 1.0 -2.0))
    (-1.0 / 2.0))
!(assertEqual
    (get-rat (better_make-rat -1.0 -2.0))
    (1.0 / 2.0))
Chunk size: 145
-----------------------------------------------------------
Final chunk: ; -----------------------End of Exercise 2.1----------------------------
Chunk size: 72
-----------------------------------------------------------
Final chunk: ; Exercise 2.2.
Chunk size: 15
-----------------------------------------------------------
Final chunk: ;
Chunk size: 1
-----------------------------------------------------------
Final chunk: ; Consider the problem of representing line segments in a plane. Each segment is
Chunk size: 80
-----------------------------------------------------------
Final chunk: ; represented as a pair of points: a starting point and an ending point. Define a constructor
Chunk size: 93
-----------------------------------------------------------
Final chunk: ; make-segment and selectors start-segment and end-segment that define the representation of
Chunk size: 92
-----------------------------------------------------------
Final chunk: ; segments in terms of points. Furthermore, a point can be represented as a pair of numbers: the x
Chunk size: 98
-----------------------------------------------------------
Final chunk: ; coordinate and the y coordinate. Accordingly, specify a constructor make-point and selectors
Chunk size: 94
-----------------------------------------------------------
Final chunk: ; x-point and y-point that define this representation. Finally, using your selectors and constructors,
Chunk size: 102
-----------------------------------------------------------
Final chunk: ; define a procedure midpoint-segment that takes a line segment as argument and returns its midpoint
Chunk size: 100
-----------------------------------------------------------
Final chunk: ; (the point whose coordinates are the average of the coordinates of the endpoints). To try your procedures,
Chunk size: 108
-----------------------------------------------------------
Final chunk: ; you'll need a way to print points
Chunk size: 35
-----------------------------------------------------------
Final chunk: (= (start-segment $seg) (first-pair $seg))
Chunk size: 42
-----------------------------------------------------------
Final chunk: (= (end-segment $seg) (second-pair $seg))
Chunk size: 41
-----------------------------------------------------------
Final chunk: (= (x-point $pt) (first-pair $pt))
Chunk size: 34
-----------------------------------------------------------
Final chunk: ; This one will print (3.0 , 4.5)
Chunk size: 33
-----------------------------------------------------------
Final chunk: ;!(print-point (midpoint-segment (make-segment (make-point 1 2) (make-point 5 7))))
Chunk size: 83
-----------------------------------------------------------
Final chunk: (= (get-point $p)
    ((x-point $p),(y-point $p)))
!(assertEqual
    (get-point (midpoint-segment (make-segment (make-point 1 2) (make-point 5 7))))
    (3.0 , 4.5))
Chunk size: 165
-----------------------------------------------------------
Final chunk: ; -----------------------End of Exercise 2.2----------------------------
Chunk size: 72
-----------------------------------------------------------
Final chunk: ; Exercise 2.3. Implement a representation for rectangles in a plane. (Hint: You may want to make use of
Chunk size: 104
-----------------------------------------------------------
Final chunk: ; exercise 2.2.) In terms of your constructors and selectors, create procedures that compute the perimeter
Chunk size: 106
-----------------------------------------------------------
Final chunk: ; and the area of a given rectangle. Now implement a different representation for rectangles. Can you
Chunk size: 101
-----------------------------------------------------------
Final chunk: ; design your system with suitable abstraction barriers, so that the same perimeter and area procedures will
Chunk size: 108
-----------------------------------------------------------
Final chunk: ; work using either representation?
Chunk size: 35
-----------------------------------------------------------
Final chunk: ; First representation of rect will be four points (top-left, top-right, bottom-left, bottom-right).
Chunk size: 100
-----------------------------------------------------------
Final chunk: (= (make-rect $top-left $top-right $bottom-left $bottom-right)
  ($bottom-left $top-left $top-right $bottom-right))
Chunk size: 115
-----------------------------------------------------------
Final chunk: (= (simple_rect) (make-rect (make-point 1 3) (make-point 2 3) (make-point 1 2) (make-point 2 2)))
!(assertEqual
    (simple_rect)
    ((1 . 2) (1 . 3) (2 . 3) (2 . 2)))
Chunk size: 168
-----------------------------------------------------------
Final chunk: (= (get-bottom-left $rect)
  (let ($bl $tl $tr $br) $rect $bl))
!(assertEqual
    (get-bottom-left (simple_rect))
    (1 . 2))
Chunk size: 126
-----------------------------------------------------------
Final chunk: (= (get-top-left $rect)
    (let ($bl $tl $tr $br) $rect $tl))
!(assertEqual
    (get-top-left (simple_rect))
    (1 . 3))
Chunk size: 122
-----------------------------------------------------------
Final chunk: (= (get-top-right $rect)
    (let ($bl $tl $tr $br) $rect $tr))
!(assertEqual
    (get-top-right (simple_rect))
    (2 . 3))
Chunk size: 124
-----------------------------------------------------------
Final chunk: (= (get-bottom-right $rect)
    (let ($bl $tl $tr $br) $rect $br))
!(assertEqual
    (get-bottom-right (simple_rect))
    (2 . 2))
Chunk size: 130
-----------------------------------------------------------
Final chunk: (= (rect-width $rect)
  (- (y-point (get-top-left $rect)) (y-point (get-bottom-left $rect))))
Chunk size: 93
-----------------------------------------------------------
Final chunk: (= (rect-height $rect)
  (- (x-point (get-top-right $rect)) (x-point (get-top-left $rect))))
Chunk size: 92
-----------------------------------------------------------
Final chunk: ; Exercise 2.6.
Chunk size: 15
-----------------------------------------------------------
Final chunk: ;
Chunk size: 1
-----------------------------------------------------------
Final chunk: ; Second representation is the top-left corner, width and height.
Chunk size: 65
-----------------------------------------------------------
Final chunk: (= (make-rect2 $top $left $width $height)
    ($top $left $width $height))
Chunk size: 74
-----------------------------------------------------------
Final chunk: (= (simple_rect2) (make-rect2 1 2 4 6))
!(assertEqual
    (simple_rect2)
    (1 2 4 6))
Chunk size: 87
-----------------------------------------------------------
Final chunk: (= (rect-height2 $rect)
    (let ($x $y $w $h) $rect
        $h))
Chunk size: 65
-----------------------------------------------------------
Final chunk: (= (rect-width2 $rect)
    (let ($x $y $w $h) $rect
        $w))
Chunk size: 64
-----------------------------------------------------------
Final chunk: (= (calc-S $rect $get-width $get-height)
  (* ($get-height $rect) ($get-width $rect)))
!(assertEqual
    (calc-S (simple_rect) rect-width rect-height)
    1)
!(assertEqual
    (calc-S (simple_rect2) rect-height2 rect-width2)
    24)
Chunk size: 232
-----------------------------------------------------------
Final chunk: (= (calc-P $rect $get-width $get-height)
  (* 2 (+ ($get-width $rect) ($get-height $rect))))
!(assertEqual
    (calc-P (simple_rect) rect-width rect-height)
    4)
!(assertEqual
    (calc-P (simple_rect2) rect-height2 rect-width2)
    20)
Chunk size: 238
-----------------------------------------------------------
Final chunk: ; -----------------------End of Exercise 2.3----------------------------
Chunk size: 72
-----------------------------------------------------------
Final chunk: (: lambda1 (-> Variable Atom (-> $a $t)))
Chunk size: 41
-----------------------------------------------------------
Final chunk: (= (cons $x $y)
  (let $dispatch (lambda1 $m
    (if (== $m 0)
        $x
        (if (== $m 1)
            $y
            (Error (cons $x $y) "Argument to cons should be only 0 or 1"))))
            $dispatch))
Chunk size: 211
-----------------------------------------------------------
Final chunk: (= (car $z) ($z 0))
!(assertEqual
    (car (cons 2 5))
    2)
Chunk size: 61
-----------------------------------------------------------
Final chunk: (= (cdr $z) ($z 1))
!(assertEqual
    (cdr (cons 2 5))
    5)
Chunk size: 61
-----------------------------------------------------------
Final chunk: ; Exercise 2.4.  Here is an alternative procedural representation of pairs. For this representation, verify that
Chunk size: 112
-----------------------------------------------------------
Final chunk: ;(car (cons x y)) yields x for any objects x and y.
Chunk size: 51
-----------------------------------------------------------
Final chunk: ;
Chunk size: 1
-----------------------------------------------------------
Final chunk: ;(define (cons x y)
Chunk size: 19
-----------------------------------------------------------
Final chunk: ;  (lambda (m) (m x y)))
Chunk size: 24
-----------------------------------------------------------
Final chunk: ;
Chunk size: 1
-----------------------------------------------------------
Final chunk: ;(define (car z)
Chunk size: 16
-----------------------------------------------------------
Final chunk: ;  (z (lambda (p q) p)))
Chunk size: 24
-----------------------------------------------------------
Final chunk: ;
Chunk size: 1
-----------------------------------------------------------
Final chunk: ; What is the corresponding definition of cdr? (Hint: To verify that this works, make use of the substitution model of s)
Chunk size: 121
-----------------------------------------------------------
Final chunk: ; section 1.
Chunk size: 12
-----------------------------------------------------------
Final chunk: (: lambda2 (-> Variable Variable Atom (-> $a $b $t)))
Chunk size: 53
-----------------------------------------------------------
Final chunk: (= (cons2 $x $y)
  (lambda1 $m ($m $x $y)))
Chunk size: 43
-----------------------------------------------------------
Final chunk: (= (car2 $z)
  ($z (lambda2 $p $q $p)))
!(assertEqual
    (car2 (cons2 5 2))
    5)
Chunk size: 83
-----------------------------------------------------------
Final chunk: (= (cdr2 $z)
  ($z (lambda2 $p $q $q)))
!(assertEqual
    (cdr2 (cons2 5 2))
    2)
Chunk size: 83
-----------------------------------------------------------
Final chunk: ; -----------------------End of Exercise 2.4----------------------------
Chunk size: 72
-----------------------------------------------------------
Final chunk: ; Exercise 2.5.
Chunk size: 15
-----------------------------------------------------------
Final chunk: ;
Chunk size: 1
-----------------------------------------------------------
Final chunk: ; Show that we can represent pairs of nonnegative integers
Chunk size: 58
-----------------------------------------------------------
Final chunk: ; using only numbers and arithmetic operations if we represent
Chunk size: 62
-----------------------------------------------------------
Final chunk: ; the pair a and b as the integer that is the product 2^a 3^b.
Chunk size: 62
-----------------------------------------------------------
Final chunk: ; Give the corresponding definitions of the procedures cons, car, and cdr.
Chunk size: 74
-----------------------------------------------------------
Final chunk: (= (even? $n)
    (== (% $n 2) 0))
Chunk size: 34
-----------------------------------------------------------
Final chunk: (= (dec $x) (- $x 1))
Chunk size: 21
-----------------------------------------------------------
Final chunk: (= (sqr $x) (* $x $x))
Chunk size: 22
-----------------------------------------------------------
Final chunk: (= (fast-exp $b $n)
    (if (== $n 0)
        1
        (if (even? $n)
            (sqr (fast-exp $b (/ $n 2)))
            (* $b (fast-exp $b (dec $n))))))
Chunk size: 156
-----------------------------------------------------------
Final chunk: (= (cons3 $a $b)
    (* (fast-exp 2 $a) (fast-exp 3 $b)))
!(assertEqual
    (cons3 1 2)
    18)
Chunk size: 95
-----------------------------------------------------------
Final chunk: (: lambda3 (-> Variable Variable Variable Atom (-> $a $b $c $t)))
Chunk size: 65
-----------------------------------------------------------
Final chunk: (= (inc $x) (+ $x 1))
Chunk size: 21
-----------------------------------------------------------
Final chunk: (= (count-factors $z $divisor)
    (let $iter (lambda3 $counter $x $self
        (if (== (% $x $divisor) 0)
            ($self (inc $counter) (/ $x $divisor) $self)
            $counter))
    ($iter 0 $z $iter)))
Chunk size: 212
-----------------------------------------------------------
Final chunk: (= (car3 $z)
    (count-factors $z 2))
!(assertEqual
    (car3 (cons3 1 2))
    1)
Chunk size: 82
-----------------------------------------------------------
Final chunk: (= (cdr3 $z)
    (count-factors $z 3))
!(assertEqual
    (cdr3 (cons3 1 2))
    2)
Chunk size: 82
-----------------------------------------------------------
Final chunk: ; -----------------------End of Exercise 2.5----------------------------
Chunk size: 72
-----------------------------------------------------------
Final chunk: ; In case representing pairs as procedures wasn't mind-boggling enough, consider that,
Chunk size: 86
-----------------------------------------------------------
Final chunk: ; in a language that can manipulate procedures, we can get by without numbers (at least insofar
Chunk size: 95
-----------------------------------------------------------
Final chunk: ; as nonnegative integers are concerned) by implementing 0 and the operation of adding 1 as
Chunk size: 91
-----------------------------------------------------------
Final chunk: ;
Chunk size: 1
-----------------------------------------------------------
Final chunk: ;(define zero (lambda (f) (lambda (x) x)))
Chunk size: 42
-----------------------------------------------------------
Final chunk: ;
Chunk size: 1
-----------------------------------------------------------
Final chunk: ;(define (add-1 n)
Chunk size: 18
-----------------------------------------------------------
Final chunk: ;  (lambda (f) (lambda (x) (f ((n f) x)))))
Chunk size: 43
-----------------------------------------------------------
Final chunk: ;
Chunk size: 1
-----------------------------------------------------------
Final chunk: ; This representation is known as Church numerals, after its inventor, Alonzo Church,
Chunk size: 85
-----------------------------------------------------------
Final chunk: ; the logician who invented the lambda calculus.
Chunk size: 48
-----------------------------------------------------------
Final chunk: ;
Chunk size: 1
-----------------------------------------------------------
Final chunk: ; Define one and two directly (not in terms of zero and add-1).
Chunk size: 63
-----------------------------------------------------------
Final chunk: ; (Hint: Use substitution to evaluate (add-1 zero)). Give a direct definition of the
Chunk size: 84
-----------------------------------------------------------
Final chunk: ; addition procedure + (not in terms of repeated application of add-1).
Chunk size: 71
-----------------------------------------------------------
Final chunk: (= (zero) (lambda1 $f (lambda1 $x $x)))
Chunk size: 39
-----------------------------------------------------------
Final chunk: (= (add-1 $n)
    (lambda1 $f
        (lambda1 $x
            ($f (($n $f) $x)))))
Chunk size: 82
-----------------------------------------------------------
Final chunk: ;So, zero is actually just not applying anything to its input.
Chunk size: 62
-----------------------------------------------------------
Final chunk: ;Zero plus one is application of input function once to the other input argument.
Chunk size: 81
-----------------------------------------------------------
Final chunk: ; So, one and two will be application of input function to input argument once and twice accordingly.
Chunk size: 101
-----------------------------------------------------------
Final chunk: (= (one)
    (lambda1 $f
        (lambda1 $x
            ($f $x))))
Chunk size: 67
-----------------------------------------------------------
Final chunk: (= (two)
    (lambda1 $f
        (lambda1 $x
            ($f ($f $x)))))
Chunk size: 72
-----------------------------------------------------------
Final chunk: (= (lsum $a $b)
    (lambda1 $f
        (lambda1 $x
            (($b $f) (($a $f) $x)))))
Chunk size: 89
-----------------------------------------------------------
Final chunk: ; -----------------------End of Exercise 2.6----------------------------
Chunk size: 72
-----------------------------------------------------------
Final chunk: ; Exercise 2.7.
Chunk size: 15
-----------------------------------------------------------
Final chunk: ;
Chunk size: 1
-----------------------------------------------------------
Final chunk: ; Alyssa's program is incomplete because she has not specified the implementation
Chunk size: 81
-----------------------------------------------------------
Final chunk: ; of the interval abstraction. Here is a definition of the interval constructor:
Chunk size: 80
-----------------------------------------------------------
Final chunk: ; (define (make-interval a b) (cons a b))
Chunk size: 41
-----------------------------------------------------------
Final chunk: ; Define selectors upper-bound and lower-bound to complete the implementation.
Chunk size: 78
-----------------------------------------------------------
Final chunk: (= (compareList $curbest $list $f)
    (if (== $list ())
        $curbest
        (let $cur (car-atom $list)
            (let $tail (cdr-atom $list)
                (if ($f $cur $curbest)
                    (compareList $cur $tail $f)
                    (compareList $curbest $tail $f))))))
Chunk size: 292
-----------------------------------------------------------
Final chunk: (= (max $varlist)
    (compareList (car-atom $varlist) $varlist >))
!(assertEqual
    (max (5 2 4 6 1))
    6)
Chunk size: 110
-----------------------------------------------------------
Final chunk: (= (min $varlist)
    (compareList (car-atom $varlist) $varlist <))
!(assertEqual
    (min (5 2 4 6 1))
    1)
Chunk size: 110
-----------------------------------------------------------
Final chunk: (= (make-interval $a $b) ($a . $b))
Chunk size: 35
-----------------------------------------------------------
Final chunk: (= (upper-bound $interval) (let ($a . $b) $interval $b))
Chunk size: 56
-----------------------------------------------------------
Final chunk: (= (lower-bound $interval) (let ($a . $b) $interval $a))
Chunk size: 56
-----------------------------------------------------------
Final chunk: (= (r1) (make-interval 0.15 0.2))
Chunk size: 33
-----------------------------------------------------------
Final chunk: (= (r2) (make-interval 0.9 1.1))
Chunk size: 32
-----------------------------------------------------------
Final chunk: (= (add-interval $x $y)
  (make-interval (+ (lower-bound $x) (lower-bound $y))
                 (+ (upper-bound $x) (upper-bound $y))))
!(assertEqual
    (add-interval (r1) (r2))
    (1.05 . 1.3))
Chunk size: 196
-----------------------------------------------------------
Final chunk: ; Define a constructor make-center-percent that takes a center and a percentage
Chunk size: 79
-----------------------------------------------------------
Final chunk: (= (div-interval $x $y)
  (mul-interval $x
                (make-interval (/ 1.0 (upper-bound $y))
                               (/ 1.0 (lower-bound $y)))))
!(assertEqual
    (div-interval (r1) (r2))
    (0.13636363636363635 . 0.22222222222222224))
Chunk size: 249
-----------------------------------------------------------
Final chunk: ; -----------------------End of Exercise 2.7----------------------------
Chunk size: 72
-----------------------------------------------------------
Final chunk: ; Exercise 2.8.
Chunk size: 15
-----------------------------------------------------------
Final chunk: ;
Chunk size: 1
-----------------------------------------------------------
Final chunk: ; Using reasoning analogous to Alyssa's, describe how the difference of two
Chunk size: 75
-----------------------------------------------------------
Final chunk: ; intervals may be computed. Define a corresponding subtraction procedure, called sub-interval.
Chunk size: 95
-----------------------------------------------------------
Final chunk: (= (sub-interval $x $y)
    (make-interval (- (lower-bound $x) (lower-bound $y))
                   (- (upper-bound $x) (upper-bound $y))))
!(assertEqual
    (sub-interval (r2) (r1))
    (0.75 . 0.9000000000000001))
Chunk size: 215
-----------------------------------------------------------
Final chunk: ; -----------------------End of Exercise 2.8----------------------------
Chunk size: 72
-----------------------------------------------------------
Final chunk: ; Exercise 2.9.
Chunk size: 15
-----------------------------------------------------------
Final chunk: ;
Chunk size: 1
-----------------------------------------------------------
Final chunk: ; The width of an interval is half of the difference between its upper and lower bounds.
Chunk size: 88
-----------------------------------------------------------
Final chunk: ; The width is a measure of the uncertainty of the number specified by the interval.
Chunk size: 84
-----------------------------------------------------------
Final chunk: ; For some arithmetic operations the width of the result of combining two intervals
Chunk size: 83
-----------------------------------------------------------
Final chunk: ; is a function only of the widths of the argument intervals, whereas for others the width
Chunk size: 90
-----------------------------------------------------------
Final chunk: ; of the combination is not a function of the widths of the argument intervals. Show that
Chunk size: 89
-----------------------------------------------------------
Final chunk: ; the width of the sum (or difference) of two intervals is a function only of the widths
Chunk size: 88
-----------------------------------------------------------
Final chunk: ; of the intervals being added (or subtracted). Give examples to show that this is not true
Chunk size: 91
-----------------------------------------------------------
Final chunk: ; for multiplication or division.
Chunk size: 33
-----------------------------------------------------------
Final chunk: (= (interval-width $interval)
    (/ (- (upper-bound $interval) (lower-bound $interval)) 2))
!(assertEqual
    (interval-width (r2))
    0.10000000000000003)
Chunk size: 157
-----------------------------------------------------------
Final chunk: ; Well, width of sum-intervals indeed equal to sum of widths, but due to rounding inside metta I can't directly compare
Chunk size: 119
-----------------------------------------------------------
Final chunk: ; results using assertEqual. Thanks to Vitaly's advice, we can use cmp-float to do that.
Chunk size: 88
-----------------------------------------------------------
Final chunk: ; -----------------------End of Exercise 2.10---------------------------
Chunk size: 72
-----------------------------------------------------------
Final chunk: ; Same here
Chunk size: 11
-----------------------------------------------------------
Final chunk: ; Exercise 2.11.
Chunk size: 16
-----------------------------------------------------------
Final chunk: ; Different results for multiplication and division:
Chunk size: 52
-----------------------------------------------------------
Final chunk: ; In passing, Ben also cryptically comments: ``By testing the signs of the endpoints of the intervals,
Chunk size: 102
-----------------------------------------------------------
Final chunk: (= (cmp-float $a $b)
    (let $diff (- $a $b)
        (if (< (Abs $diff) 1e-10) EQ
            (if (< $diff 0) LT GT))))
!(assertEqual
    (cmp-float (interval-width (add-interval (r1) (r2))) (+ (interval-width (r2)) (interval-width (r1))))
    EQ)
!(assertEqual
    (cmp-float (interval-width (sub-interval (r2) (r1))) (- (interval-width (r2)) (interval-width (r1))))
    EQ)
Chunk size: 376
-----------------------------------------------------------
Final chunk: !(assertEqual
    (cmp-float (interval-width (div-interval (r2) (r1))) (/ (interval-width (r2)) (interval-width (r1))))
    LT)
Chunk size: 127
-----------------------------------------------------------
Final chunk: ; -----------------------End of Exercise 2.9----------------------------
Chunk size: 72
-----------------------------------------------------------
Final chunk: ; Exercise 2.10.
Chunk size: 16
-----------------------------------------------------------
Final chunk: ;
Chunk size: 1
-----------------------------------------------------------
Final chunk: ; Ben Bitdiddle, an expert systems programmer, looks over Alyssa's shoulder and
Chunk size: 79
-----------------------------------------------------------
Final chunk: ; comments that it is not clear what it means to divide by an interval that spans zero.
Chunk size: 87
-----------------------------------------------------------
Final chunk: ; Modify Alyssa's code to check for this condition and to signal an error if it occurs.
Chunk size: 87
-----------------------------------------------------------
Final chunk: ; it is possible to break mul-interval into nine cases, only one of which requires more than two
Chunk size: 96
-----------------------------------------------------------
Final chunk: (= (r3) (make-interval -0.4 0.5))
Chunk size: 33
-----------------------------------------------------------
Final chunk: ; multiplications.'' Rewrite this procedure using Ben's suggestion.
Chunk size: 67
-----------------------------------------------------------
Final chunk: (= (and4 $a $b $c $d) (and (and $a $b) (and $c $d)))
Chunk size: 52
-----------------------------------------------------------
Final chunk: (
=
(better-mul-interval $int1 $int2)
(
let*
(
    ($x1 (lower-bound $int1))
    ($x2 (lower-bound $int2))
    ($y1 (upper-bound $int1))
    ($y2 (upper-bound $int2))
  )
Chunk size: 170
-----------------------------------------------------------
Final chunk: (
if
(and4 (< $x1 0) (>= $y1 0) (< $x2 0) (>= $y2 0))
(make-interval (min ((* $x1 $y2) (* $y1 $x2))) (* $y1 $y2))
(
if
(and4 (< $x1 0) (< $y1 0) (< $x2 0) (>= $y2 0))
(make-interval (* $y1 $y2) (* $y1 $x2))
(
if
(and4 (>= $x1 0) (>= $y1 0) (< $x2 0) (>= $y2 0))
(make-interval (* $y1 $x2) (* $y1 $y2))
(
if
(and4 (< $x1 0) (>= $y1 0) (< $x2 0) (< $y2 0))
(make-interval (* $y1 $y2) (* $x1 $y2))
(
if
(and4 (< $x1 0) (< $y1 0) (< $x2 0) (< $y2 0))
(make-interval (* $y1 $y2) (* $x1 $x2))
Chunk size: 486
-----------------------------------------------------------
Final chunk: (if (and4 (>= $x1 0) (>= $y1 0) (< $x2 0) (< $y2 0))
        (make-interval (* $y1 $y2) (* $x1 $x2))
    (if (and4 (< $x1 0) (>= $y1 0) (>= $x2 0) (>= $y2 0))
        (make-interval (* $x1 $y2) (* $y1 $y2))
    (if (and4 (< $x1 0) (< $y1 0) (>= $x2 0) (>= $y2 0))
        (make-interval (* $y1 $y2) (* $x1 $x2))
    (if (and4 (>= $x1 0) (>= $y1 0) (>= $x2 0) (>= $y2 0))
        (make-interval (* $x1 $x2) (* $y1 $y2))
        (Error (better-mul-interval $int1 $int2) "Unknown variant")))))
)
)
)
)
)
Chunk size: 500
-----------------------------------------------------------
Final chunk: )
)
Chunk size: 3
-----------------------------------------------------------
Final chunk: (= (mul-interval $x $y)
  (let*
  (
    ($p1 (* (lower-bound $x) (lower-bound $y)))
    ($p2 (* (lower-bound $x) (upper-bound $y)))
    ($p3 (* (upper-bound $x) (lower-bound $y)))
    ($p4 (* (upper-bound $x) (upper-bound $y)))
  )
    (make-interval (min ($p1 $p2 $p3 $p4))
                   (max ($p1 $p2 $p3 $p4)))))
!(assertEqual
    (mul-interval (r1) (r2))
    (0.135 . 0.22000000000000003))
!(assertEqual
    (mul-interval (r3) (r2))
    (better-mul-interval (r3) (r2)))
Chunk size: 478
-----------------------------------------------------------
Final chunk: ; -----------------------End of Exercise 2.11---------------------------
Chunk size: 72
-----------------------------------------------------------
Final chunk: ; For interval presented in the following form: 3.5 +- 0.15:
Chunk size: 60
-----------------------------------------------------------
Final chunk: (= (make-center-width $c $w)
    (make-interval (- $c $w) (+ $c $w)))
Chunk size: 69
-----------------------------------------------------------
Final chunk: (= (center $i)
    (/ (+ (lower-bound $i) (upper-bound $i)) 2))
Chunk size: 63
-----------------------------------------------------------
Final chunk: ; Exercise 2.12.
Chunk size: 16
-----------------------------------------------------------
Final chunk: ; tolerance and produces the desired interval. You must also define a selector
Chunk size: 78
-----------------------------------------------------------
Final chunk: ; percent that produces the percentage tolerance for a given interval. The center
Chunk size: 81
-----------------------------------------------------------
Final chunk: ; selector is the same as the one shown above.
Chunk size: 46
-----------------------------------------------------------
Final chunk: (= (make-center-percent $mid $percent-deviance)
    (let $dev (* (/ $percent-deviance 100.0) $mid)
        (make-interval (- $mid $dev) (+ $mid $dev))))
!(assertEqual
    (make-center-percent 6 15)
    (5.1 . 6.9))
Chunk size: 214
-----------------------------------------------------------
Final chunk: (= (percent $interval)
    (let $cntr (center $interval)
        (* (/ (- (upper-bound $interval) $cntr) $cntr) 100)))
!(assertEqual
    (percent (make-center-percent 6 15))
    15.000000000000005)
Chunk size: 197
-----------------------------------------------------------
Final chunk: ; -----------------------End of Exercise 2.12---------------------------
Chunk size: 72
-----------------------------------------------------------
Final chunk: ; Exercise 2.14.
Chunk size: 16
-----------------------------------------------------------
Final chunk: ;
Chunk size: 1
-----------------------------------------------------------
Final chunk: ; based on already defined methods for interval arithmetic we can try to calculate
Chunk size: 82
-----------------------------------------------------------
Final chunk: ; resistance of two parallel resistors in two ways.
Chunk size: 51
-----------------------------------------------------------
Final chunk: ; Lem complains that Alyssa's program gives different answers for the two ways of computing. This is a serious complaint.
Chunk size: 121
-----------------------------------------------------------
Final chunk: ; Demonstrate that Lem is right. Investigate the behavior of the system on a variety of arithmetic expressions.
Chunk size: 111
-----------------------------------------------------------
Final chunk: ; Make some intervals A and B, and use them in computing the expressions A/A and A/B. You will get the most insight
Chunk size: 115
-----------------------------------------------------------
Final chunk: ; by using intervals whose width is a small percentage of the center value.
Chunk size: 75
-----------------------------------------------------------
Final chunk: ; Examine the results of the computation in center-percent form (see exercise 2.12).
Chunk size: 84
-----------------------------------------------------------
Final chunk: (= (r_c1) (make-center-percent 10 1))
Chunk size: 37
-----------------------------------------------------------
Final chunk: (= (r_c2) (make-center-percent 100 1))
Chunk size: 38
-----------------------------------------------------------
Final chunk: (= (small-width-r1) (make-center-percent 10 0.01))
Chunk size: 50
-----------------------------------------------------------
Final chunk: (= (small-width-r2) (make-center-percent 100 0.01))
Chunk size: 51
-----------------------------------------------------------
Final chunk: ; Indeed, results are different.
Chunk size: 32
-----------------------------------------------------------
Final chunk: (= (par1 $r1 $r2)
    (div-interval (mul-interval $r1 $r2)
    (add-interval $r1 $r2)))
!(assertEqual
    (par1 (r_c1) (r_c2))
    (8.821782178217822 . 9.367309458218548))
!(assertEqual
    (par1 (small-width-r1) (small-width-r2))
    (9.088182181781821 . 9.093636727309095))
Chunk size: 275
-----------------------------------------------------------
Final chunk: (= (par2 $r1 $r2)
    (let $one (make-interval 1 1)
        (div-interval $one
            (add-interval (div-interval $one $r1)
            (div-interval $one $r2)))))
!(assertEqual
    (par2 (r_c1) (r_c2))
    (9.0 . 9.181818181818182))
!(assertEqual
    (par2 (small-width-r1) (small-width-r2))
    (9.090000000000002 . 9.091818181818182))
Chunk size: 342
-----------------------------------------------------------
Final chunk: ; Compute A/A
Chunk size: 13
-----------------------------------------------------------
Final chunk: ; Compute A/B
Chunk size: 13
-----------------------------------------------------------
Final chunk: (= (better-div-interval $x $y)
    (if (or (and (< (upper-bound $y) 0) (> (lower-bound $y) 0))
             (and (< (lower-bound $y) 0) (> (upper-bound $y) 0)))
        (Error (better-div-interval $x $y) "Divisor interval spans zero")
        (mul-interval $x
                (make-interval (/ 1.0 (upper-bound $y))
                               (/ 1.0 (lower-bound $y))))))
!(assertEqual
    (better-div-interval (r1) (r2))
    (0.13636363636363635 . 0.22222222222222224))
Chunk size: 474
-----------------------------------------------------------
Final chunk: !(assertEqual
    (better-div-interval (r_c1) (r_c1))
    (0.9801980198019803 . 1.02020202020202))
!(assertEqual
    (better-div-interval (r_c2) (r_c2))
    (0.9801980198019802 . 1.0202020202020203))
!(assertEqual
    (better-div-interval (small-width-r1) (small-width-r1))
    (0.9998000199980004 . 1.000200020002))
!(assertEqual
    (better-div-interval (small-width-r2) (small-width-r2))
    (0.9998000199980001 . 1.0002000200020003))
Chunk size: 437
-----------------------------------------------------------
Final chunk: !(assertEqual
    (better-div-interval (small-width-r1) (small-width-r2))
    (0.09998000199980002 . 0.10002000200020002))
Chunk size: 122
-----------------------------------------------------------
Final chunk: ; So, the smaller the width of interval, the preciser the results.
Chunk size: 66
-----------------------------------------------------------
Final chunk: ; -----------------------End of Exercise 2.14---------------------------
Chunk size: 72
-----------------------------------------------------------
```