(define (problem aliens11)
	(:domain aliens1)
	(:init
		(= (ship-x) 40.0)
		(drone2-first-undock)
		(= (drone2-x) 40.0)
		(= (drone1-y) 700.0)
		(= (ship-y) 700.0)
		(first-time)
		(= (drone2-y) 700.0)
		(drone1-first-undock)
		(p1_0)
		(= (drone1-x) 40.0)
	)
	(:goal (and
		(london-bombed)
		(p1)
	)
)
)
(:metric minimize (+
		(* 1 (total-time))
)
)
