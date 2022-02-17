(define (problem aliens1)
	(:domain aliens)

	(:init 
		(first-time)
		(drone1-first-undock)
		(drone2-first-undock)
		(= (ship-x) 40.0)
		(= (ship-y) 700.0)
		(= (drone1-x) 40.0)
		(= (drone1-y) 700.0)
		(= (drone2-x) 40.0)
		(= (drone2-y) 700.0)
	)

	(:goal (and
		; (above-whitehouse)
		(london-bombed)
		)
	)
)

(:metric minimize (+
					(* 1 (total-time) ))
)
