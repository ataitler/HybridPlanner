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
		(= (drone1-battery) 1600.0)
		(= (drone2-battery) 1600.0)
		(= (ship-battery) 2000.0)
	)

	(:goal (and
		(above-whitehouse)
		)
	)
)

(:metric minimize (+
					(* -0.1 (drone1-battery))
					(* -0.1 (drone2-battery))
					(* -0.1 (ship-battery)) 
					(* 20 (total-time) ))
)
