(define (domain aliens)
	(:requirements :typing :durative-actions :fluents :duration-inequalities)

	(:predicates
		(ny-bombed)
		(sf-bombed)
		(paris-bombed)
		(rome-bombed)
		(london-bombed)
		(above-whitehouse)
		(invasion-ongoing)
		(ship-fly)
		(ship-fly-none)
		(ship-fly-one)
		(ship-fly-two)
		(drone1-fly)
		(drone1-undocking)
		(drone2-fly)
		(drone2-undocking)
		(invasion-started)
		(first-time)
		(drone1-first-undock)
		(drone2-first-undock)
		(drone2-busy)
		(drone1-busy)
	)

	(:functions
		(ship-x)
		(ship-y)
		(ship-battery)
		(drone1-x)
		(drone1-y)
		(drone1-battery)
		(drone2-x)
		(drone2-y)
		(drone2-battery)
	)


	(:control-variable warp-speed
		:bounds (and (>= ?value -10000000.0) (<= ?value 10000000.0))
	)

	(:control-variable vx-ship
		:bounds (and (>= ?value -20.0) (<= ?value 20.0))
	)

	(:control-variable vy-ship
		:bounds (and (>= ?value -20.0) (<= ?value 20.0))
	)

	(:control-variable vx-drone1
		:bounds (and (>= ?value -20.0) (<= ?value 20.0))
	)

	(:control-variable vy-drone1
		:bounds (and (>= ?value -20.0) (<= ?value 20.0))
	)

	(:control-variable vx-drone2
		:bounds (and (>= ?value -20.0) (<= ?value 20.0))
	)

	(:control-variable vy-drone2
		:bounds (and (>= ?value -20.0) (<= ?value 20.0))
	)

	(:control-variable-vector energy-drone1
		:control-variables ((vx-drone1) (vy-drone1))
		:max-norm 800
	)


	(:control-variable-vector energy-drone2
		:control-variables ((vx-drone2) (vy-drone2))
		:max-norm 800
	)

	(:control-variable-vector energy-ship
		:control-variables ((vx-ship) (vy-ship))
		:max-norm 800
	)



	(:region earth
		:parameters (?x ?y)
		:condition (and (in-rect (?x ?y) :corner (0 0) :width 1280 :height 1024))
	)

	(:region london-region
		:parameters (?x ?y)
		:condition (and (in-rect (?x ?y) :corner (92 182) :width 32 :height 32))
	)

	(:region paris-region
		:parameters (?x ?y)
		:condition (and (in-rect (?x ?y) :corner (732 82) :width 32 :height 32))
	)

	(:region rome-region
		:parameters (?x ?y)
		:condition (and (in-rect (?x ?y) :corner (332 382) :width 32 :height 32))
	)

	(:region sf-region
		:parameters (?x ?y)
		:condition (and (in-rect (?x ?y) :corner (1132 102) :width 32 :height 32))
	)

	(:region ny-region
		:parameters (?x ?y)
		:condition (and (in-rect (?x ?y) :corner (682 782) :width 32 :height 32))
	)

	(:region wdc-region
		:parameters (?x ?y)
		:condition (and (in-rect (?x ?y) :corner (982 482) :width 32 :height 32))
	)

	(:region ship-range
		:parameters (?x1 ?y1 ?x2 ?y2)
		:condition (and (max-distance ((?x1 ?y1) (?x2 ?y2)) :d 24))
	)


	; start the invasion, this action starts the plan
	(:durative-action start-invasion
		:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
		:condition (and
			(at start (not (invasion-ongoing)))
			(at start (not (london-bombed)))
			(at start (not (paris-bombed)))
			(at start (not (rome-bombed)))
			(at start (not (sf-bombed)))
			(at start (not (ny-bombed)))
			(at start (first-time))
			(at start (not (invasion-started)))
		)
		:effect (and
			(at start (not (first-time)))
			(at end (invasion-ongoing))
		)
	)



	;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	;	ship fly actions
	;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

	; ship fly with non of the drones on board
	(:durative-action fly-ship
		:duration (and (>= ?duration 0.1) (<= ?duration 200.0))
		:condition (and 
			(over all (invasion-ongoing))
			(over all (inside (earth (ship-x) (ship-y))))
			(at start (not (ship-fly)))
			(at start (not (invasion-started)))
			(over all (>= (ship-battery) 0))
		)
		:effect (and
			(increase (ship-x) (* (vx-ship) #t))
			(increase (ship-y) (* (vy-ship) #t))
			(at start (ship-fly))
			(at end (not (ship-fly)))
			(at start (invasion-started))
			(decrease (ship-battery) (* 1.0 (norm (energy-ship)) #t))
		)
	)


	;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	;	drone1 fly actions
	;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

	(:durative-action undock-drone1
		:duration (and (>= ?duration 0.01) (<= ?duration 0.03))
		:condition (and
			(at start (invasion-ongoing))
			(at end (invasion-ongoing))
			(at start (ship-fly))
			(over all (ship-fly))
			(at end (ship-fly))
			(at start (drone1-first-undock))
			
			(at start (not (drone1-fly)))
			(at start (not (drone1-undocking)))
			(at end (inside (ship-range (ship-x) (ship-y) (drone1-x) (drone1-y))))
			(at end (drone1-fly))
		)
		:effect (and
			(at start (drone1-undocking))
			(at end (not (drone1-undocking)))
			(at end (not (drone1-first-undock)))
			(increase (drone1-x) (* (warp-speed) #t))
			(increase (drone1-y) (* (warp-speed) #t))
		)
	)


	(:durative-action fly-drone1
		:duration (and (>= ?duration 0.1) (<= ?duration 200.0))
		:condition (and
			(at start (invasion-ongoing))
			(at end (invasion-ongoing))
			(at start (ship-fly))
			(over all (ship-fly))
			(at end (ship-fly))
			(at start (inside (earth (drone1-x) (drone1-y))))
			(over all (inside (earth (drone1-x) (drone1-y))))

			(at start (drone1-undocking))
			(at start (not (drone1-fly)))
			(over all (inside (earth (drone1-x) (drone1-y))))
			(at start (inside (ship-range (ship-x) (ship-y) (drone1-x) (drone1-y))))
			(at end (inside (ship-range (ship-x) (ship-y) (drone1-x) (drone1-y))))

			(over all (>= (drone1-battery) 0))
		)
		:effect (and
			(at start (drone1-fly))
			(at end (not (drone1-fly)))
			(increase (drone1-x) (* (vx-drone1) #t))
			(increase (drone1-y) (* (vy-drone1) #t))
			(decrease (drone1-battery) (* 1.0 (norm (energy-drone1)) #t))
		)
	)


	;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	;	drone2 fly actions
	;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

	(:durative-action undock-drone2
		:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
		:condition (and
			(at start (invasion-ongoing))
			(at end (invasion-ongoing))
			(at start (ship-fly))
			(over all (ship-fly))
			(at end (ship-fly))
			(at start (drone2-first-undock))
			
			(at start (not (drone2-fly)))
			(at start (not (drone2-undocking)))
			(at end (inside (ship-range (ship-x) (ship-y) (drone2-x) (drone2-y))))
			(at end (drone2-fly))
		)
		:effect (and
			(at start (drone2-undocking))
			(at end (not (drone2-undocking)))
			(at end (not (drone2-first-undock)))
			(increase (drone2-x) (* (warp-speed) #t))
			(increase (drone2-y) (* (warp-speed) #t))
		)
	)


	(:durative-action fly-drone2
		:duration (and (>= ?duration 0.1) (<= ?duration 200.0))
		:condition (and
			(at start (invasion-ongoing))
			(at end (invasion-ongoing))
			(at start (ship-fly))
			(over all (ship-fly))
			(at end (ship-fly))
			(at start (inside (earth (drone2-x) (drone2-y))))
			(over all (inside (earth (drone2-x) (drone2-y))))

			(at start (drone2-undocking))
			(at start (not (drone2-fly)))
			(over all (inside (earth (drone2-x) (drone2-y))))
			(at start (inside (ship-range (ship-x) (ship-y) (drone2-x) (drone2-y))))
			(at end (inside (ship-range (ship-x) (ship-y) (drone2-x) (drone2-y))))

			(over all (>= (drone2-battery) 0))
		)
		:effect (and
			(at start (drone2-fly))
			(at end (not (drone2-fly)))
			(increase (drone2-x) (* (vx-drone2) #t))
			(increase (drone2-y) (* (vy-drone2) #t))
			(decrease (drone2-battery) (* 1.0 (norm (energy-drone2)) #t))
		)
	)



	;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	;	drone1 bomb actions
	;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


	(:durative-action bomb-london1
		:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
		:condition (and
			(at start not (drone1-busy))
			(at end (drone1-busy))
			(over all (invasion-ongoing))
			(at start (drone1-fly))
			(at end (drone1-fly))
			(over all (drone1-fly))
			(at start (not (london-bombed)))
			(over all (inside (london-region (drone1-x) (drone1-y) )))
			(over all (invasion-ongoing))
		)
		:effect (and
			(at start (drone1-busy))
			(at end (not (drone1-busy)))
			(at end (london-bombed))
		)
	)

	(:durative-action bomb-paris1
		:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
		:condition (and
			(at start not (drone1-busy))
			(at end (drone1-busy))
			(at start (drone1-fly))
			(at end (drone1-fly))
			(over all (drone1-fly))
			(at start (not (paris-bombed)))
			(over all (inside (paris-region (drone1-x) (drone1-y) )))
			(over all (invasion-ongoing))
		)
		:effect (and
			(at start (drone1-busy))
			(at end (not (drone1-busy)))
			(at end (paris-bombed))
		)
	)

	(:durative-action bomb-rome1
		:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
		:condition (and
			(at start not (drone1-busy))
			(at end (drone1-busy))
			(at start (drone1-fly))
			(at end (drone1-fly))
			(over all (drone1-fly))
			(at start (not (rome-bombed)))
			(over all (inside (rome-region (drone1-x) (drone1-y) )))
			(over all (invasion-ongoing))
		)
		:effect (and
			(at start (drone1-busy))
			(at end (not (drone1-busy)))
			(at end (rome-bombed))
		)
	)

	(:durative-action bomb-ny1
		:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
		:condition (and
			(at start not (drone1-busy))
			(at end (drone1-busy))
			(at start (drone1-fly))
			(at end (drone1-fly))
			(over all (drone1-fly))
			(at start (not (ny-bombed)))
			(over all (inside (ny-region (drone1-x) (drone1-y) )))
			(over all (invasion-ongoing))
		)
		:effect (and
			(at start (drone1-busy))
			(at end (not (drone1-busy)))
			(at end (ny-bombed))
		)
	)

	(:durative-action bomb-sf1
		:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
		:condition (and
			(at start not (drone1-busy))
			(at end (drone1-busy))
			(at start (drone1-fly))
			(at end (drone1-fly))
			(over all (drone1-fly))
			(at start (not (sf-bombed)))
			(over all (inside (sf-region (drone1-x) (drone1-y) )))
			(over all (invasion-ongoing))
		)
		:effect (and
			(at start (drone1-busy))
			(at end (not (drone1-busy)))
			(at end (sf-bombed))
		)
	)

	;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	;	drone1 bomb actions
	;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

	(:durative-action bomb-london2
		:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
		:condition (and
			(at start not (drone2-busy))
			(at end (drone2-busy))
			(at start (drone2-fly))
			(at end (drone2-fly))
			(over all (drone2-fly))
			(at start (not (london-bombed)))
			(over all (inside (london-region (drone2-x) (drone2-y) )))
			(over all (invasion-ongoing))
		)
		:effect (and
			(at start (drone2-busy))
			(at end (not (drone2-busy)))
			(at end (london-bombed))
		)
	)

	(:durative-action bomb-paris2
		:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
		:condition (and
			(at start not (drone2-busy))
			(at end (drone2-busy))
			(at start (drone2-fly))
			(at end (drone2-fly))
			(over all (drone2-fly))
			(at start (not (paris-bombed)))
			(over all (inside (paris-region (drone2-x) (drone2-y) )))
			(over all (invasion-ongoing))
		)
		:effect (and
			(at start (drone2-busy))
			(at end (not (drone2-busy)))
			(at end (paris-bombed))
		)
	)

	(:durative-action bomb-rome2
		:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
		:condition (and
			(at start not (drone2-busy))
			(at end (drone2-busy))
			(at start (drone2-fly))
			(at end (drone2-fly))
			(over all (drone2-fly))
			(at start (not (rome-bombed)))
			(over all (inside (rome-region (drone2-x) (drone2-y) )))
			(over all (invasion-ongoing))
		)
		:effect (and
			(at start (drone2-busy))
			(at end (not (drone2-busy)))
			(at end (rome-bombed))
		)
	)

	(:durative-action bomb-ny2
		:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
		:condition (and
			(at start not (drone2-busy))
			(at end (drone2-busy))
			(at start (drone2-fly))
			(at end (drone2-fly))
			(over all (drone2-fly))
			(at start (not (ny-bombed)))
			(over all (inside (ny-region (drone2-x) (drone2-y) )))
			(over all (invasion-ongoing))
		)
		:effect (and
			(at start (drone2-busy))
			(at end (not (drone2-busy)))
			(at end (ny-bombed))
		)
	)

	(:durative-action bomb-sf2
		:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
		:condition (and
			(at start not (drone2-busy))
			(at end (drone2-busy))
			(at start (drone2-fly))
			(at end (drone2-fly))
			(over all (drone2-fly))
			(at start (not (sf-bombed)))
			(over all (inside (sf-region (drone2-x) (drone2-y) )))
			(over all (invasion-ongoing))
		)
		:effect (and
			(at start (drone2-busy))
			(at end (not (drone2-busy)))
			(at end (sf-bombed))
		)
	)


	; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	; ;	threat whitehouse
	; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

	(:durative-action threat-whitehouse
		:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
		:condition (and
			(over all (inside (wdc-region (ship-x) (ship-y) )))
			(at start (london-bombed))
			(at start (paris-bombed))
			(at start (rome-bombed))
			(at start (ny-bombed))
			(at start (sf-bombed))
		)
		:effect (and
			(at end (not (invasion-ongoing)))
			(at end (above-whitehouse))
		)
	)

)
































