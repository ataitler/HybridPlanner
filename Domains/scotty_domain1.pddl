(define (domain aliens1)
(:requirements :typing :durative-actions :fluents :duration-inequalities)

(:predicates
	(p1_2)
	(ship-fly-two)
	(drone1-undocking)
	(drone2-first-undock)
	(paris-bombed)
	(p1_3)
	(p1_6)
	(ship-fly-none)
	(p1_8)
	(p1_4)
	(invasion-ongoing)
	(invasion-started)
	(p1_1)
	(sf-bombed)
	(drone1-fly)
	(first-time)
	(drone1-busy)
	(p1_10)
	(p1_7)
	(above-whitehouse)
	(p1_5)
	(p1_9)
	(drone2-fly)
	(p1)
	(ship-fly)
	(drone2-undocking)
	(p1_0)
	(london-bombed)
	(ship-fly-one)
	(drone1-first-undock)
	(rome-bombed)
	(drone2-busy)
	(ny-bombed)
)

(:functions
	(ship-x)
	(drone2-x)
	(drone1-y)
	(ship-y)
	(drone1-x)
	(drone2-y)
)

(:control-variable vy-ship
	:bounds (and (>= ?value -20.0) (<= ?value 20.0))
)
(:control-variable vy-drone2
	:bounds (and (>= ?value -20.0) (<= ?value 20.0))
)
(:control-variable vx-drone1
	:bounds (and (>= ?value -20.0) (<= ?value 20.0))
)
(:control-variable vx-drone2
	:bounds (and (>= ?value -20.0) (<= ?value 20.0))
)
(:control-variable vx-ship
	:bounds (and (>= ?value -20.0) (<= ?value 20.0))
)
(:control-variable warp-speed
	:bounds (and (>= ?value -10000000.0) (<= ?value 10000000.0))
)
(:control-variable vy-drone1
	:bounds (and (>= ?value -20.0) (<= ?value 20.0))
)


(:region ny-region
	:parameters (?x ?y)
	:condition (and (in-rect (?x ?y) :corner (682 782) :width 32 :height 32))
)
(:region ship-range
	:parameters (?x1 ?y1 ?x2 ?y2)
	:condition (and (max-distance ((?x1 ?y1) (?x2 ?y2)) :d 24))
)
(:region rome-region
	:parameters (?x ?y)
	:condition (and (in-rect (?x ?y) :corner (332 382) :width 32 :height 32))
)
(:region paris-region
	:parameters (?x ?y)
	:condition (and (in-rect (?x ?y) :corner (732 82) :width 32 :height 32))
)
(:region earth
	:parameters (?x ?y)
	:condition (and (in-rect (?x ?y) :corner (0 0) :width 1280 :height 1024))
)
(:region sf-region
	:parameters (?x ?y)
	:condition (and (in-rect (?x ?y) :corner (1132 102) :width 32 :height 32))
)
(:region wdc-region
	:parameters (?x ?y)
	:condition (and (in-rect (?x ?y) :corner (982 482) :width 32 :height 32))
)
(:region london-region
	:parameters (?x ?y)
	:condition (and (in-rect (?x ?y) :corner (92 182) :width 32 :height 32))
)

(:durative-action start-invasion_121
	:parameters ()
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
		(at start (not (p1)))
		(at start (not (p1_0)))
	)
	:effect (and
		(at start (not (first-time)))
		(at end (invasion-ongoing))
		(at start (p1))
	)
)
(:durative-action start-invasion_131
	:parameters ()
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
		(at start (not (p1)))
		(at end (p1))
		(at start (p1_0))
	)
	:effect (and
		(at start (not (first-time)))
		(at end (invasion-ongoing))
		(at start (not (p1_0)))
		(at start (p1_1))
	)
)
(:durative-action start-invasion_141
	:parameters ()
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
		(at start (not (p1)))
		(at end (not (p1)))
		(at start (p1_0))
		(at end (not (p1_1)))
	)
	:effect (and
		(at start (not (first-time)))
		(at end (invasion-ongoing))
		(at start (not (p1_0)))
		(at start (p1_1))
		(at end (p1))
	)
)
(:durative-action fly-ship_131
	:parameters ()
	:duration (and (>= ?duration 0.1) (<= ?duration 200.0))
	:condition (and
		(over all (invasion-ongoing))
		(over all (inside (earth (ship-x) (ship-y))))
		(at start (not (ship-fly)))
		(at start (not (invasion-started)))
		(at start (not (p1)))
		(at end (p1))
		(at start (p1_2))
	)
	:effect (and
		(increase (ship-x) (* 1 (vx-ship) #t))
		(increase (ship-y) (* 1 (vy-ship) #t))
		(at start (ship-fly))
		(at end (not (ship-fly)))
		(at start (invasion-started))
		(at start (not (p1_2)))
		(at start (p1_3))
	)
)
(:durative-action bomb-ny1_101
	:parameters ()
	:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
	:condition (and
		(at start (not (drone1-busy)))
		(at end (drone1-busy))
		(at start (drone1-fly))
		(at end (drone1-fly))
		(over all (drone1-fly))
		(at start (not (ny-bombed)))
		(over all (inside (ny-region (drone1-x) (drone1-y))))
		(over all (invasion-ongoing))
	)
	:effect (and
		(at start (drone1-busy))
		(at end (not (drone1-busy)))
		(at end (ny-bombed))
		(at start (p1))
	)
)
(:durative-action fly-drone2_121
	:parameters ()
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
		(at end (not (drone2-busy)))
		(at start (not (p1)))
		(at start (not (p1_4)))
	)
	:effect (and
		(at start (drone2-fly))
		(at end (not (drone2-fly)))
		(increase (drone2-x) (* 1 (vx-drone2) #t))
		(increase (drone2-y) (* 1 (vy-drone2) #t))
		(at start (p1))
	)
)
(:durative-action undock-drone2_151
	:parameters ()
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
		(at start (not (p1)))
		(at end (not (p1)))
		(at start (p1_3))
		(at end (p1_5))
	)
	:effect (and
		(at start (drone2-undocking))
		(at end (not (drone2-undocking)))
		(at end (not (drone2-first-undock)))
		(increase (drone2-x) (* 1 (warp-speed) #t))
		(increase (drone2-y) (* 1 (warp-speed) #t))
		(at start (not (p1_3)))
		(at start (p1_4))
		(at end (not (p1_5)))
		(at end (p1_6))
	)
)
(:durative-action bomb-london2_111
	:parameters ()
	:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
	:condition (and
		(at start (not (drone2-busy)))
		(at end (drone2-busy))
		(at start (drone2-fly))
		(at end (drone2-fly))
		(over all (drone2-fly))
		(at start (not (london-bombed)))
		(over all (inside (london-region (drone2-x) (drone2-y))))
		(over all (invasion-ongoing))
		(at start (p1))
	)
	:effect (and
		(at start (drone2-busy))
		(at end (not (drone2-busy)))
		(at end (london-bombed))
	)
)
(:durative-action bomb-london2_151
	:parameters ()
	:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
	:condition (and
		(at start (not (drone2-busy)))
		(at end (drone2-busy))
		(at start (drone2-fly))
		(at end (drone2-fly))
		(over all (drone2-fly))
		(at start (not (london-bombed)))
		(over all (inside (london-region (drone2-x) (drone2-y))))
		(over all (invasion-ongoing))
		(at start (not (p1)))
		(at end (not (p1)))
		(at start (p1_6))
		(at end (p1_7))
	)
	:effect (and
		(at start (drone2-busy))
		(at end (not (drone2-busy)))
		(at end (london-bombed))
		(at start (not (p1_6)))
		(at start (p1_7))
		(at end (not (p1_7)))
		(at end (p1_8))
	)
)
(:durative-action bomb-paris2_101
	:parameters ()
	:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
	:condition (and
		(at start (not (drone2-busy)))
		(at end (drone2-busy))
		(at start (drone2-fly))
		(at end (drone2-fly))
		(over all (drone2-fly))
		(at start (not (paris-bombed)))
		(over all (inside (paris-region (drone2-x) (drone2-y))))
		(over all (invasion-ongoing))
	)
	:effect (and
		(at start (drone2-busy))
		(at end (not (drone2-busy)))
		(at end (paris-bombed))
		(at start (p1))
	)
)
(:durative-action fly-drone2_151
	:parameters ()
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
		(at end (not (drone2-busy)))
		(at start (not (p1)))
		(at end (not (p1)))
		(at start (p1_4))
		(at end (p1_8))
	)
	:effect (and
		(at start (drone2-fly))
		(at end (not (drone2-fly)))
		(increase (drone2-x) (* 1 (vx-drone2) #t))
		(increase (drone2-y) (* 1 (vy-drone2) #t))
		(at start (not (p1_4)))
		(at start (p1_5))
		(at end (not (p1_8)))
		(at end (p1_9))
	)
)
(:durative-action fly-drone2_131
	:parameters ()
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
		(at end (not (drone2-busy)))
		(at start (not (p1)))
		(at end (p1))
		(at start (p1_4))
	)
	:effect (and
		(at start (drone2-fly))
		(at end (not (drone2-fly)))
		(increase (drone2-x) (* 1 (vx-drone2) #t))
		(increase (drone2-y) (* 1 (vy-drone2) #t))
		(at start (not (p1_4)))
		(at start (p1_5))
	)
)
(:durative-action undock-drone2_111
	:parameters ()
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
		(at start (p1))
	)
	:effect (and
		(at start (drone2-undocking))
		(at end (not (drone2-undocking)))
		(at end (not (drone2-first-undock)))
		(increase (drone2-x) (* 1 (warp-speed) #t))
		(increase (drone2-y) (* 1 (warp-speed) #t))
	)
)
(:durative-action fly-ship_151
	:parameters ()
	:duration (and (>= ?duration 0.1) (<= ?duration 200.0))
	:condition (and
		(over all (invasion-ongoing))
		(over all (inside (earth (ship-x) (ship-y))))
		(at start (not (ship-fly)))
		(at start (not (invasion-started)))
		(at start (not (p1)))
		(at end (not (p1)))
		(at start (p1_2))
		(at end (p1_9))
	)
	:effect (and
		(increase (ship-x) (* 1 (vx-ship) #t))
		(increase (ship-y) (* 1 (vy-ship) #t))
		(at start (ship-fly))
		(at end (not (ship-fly)))
		(at start (invasion-started))
		(at start (not (p1_2)))
		(at start (p1_3))
		(at end (not (p1_9)))
		(at end (p1_10))
	)
)
(:durative-action fly-ship_111
	:parameters ()
	:duration (and (>= ?duration 0.1) (<= ?duration 200.0))
	:condition (and
		(over all (invasion-ongoing))
		(over all (inside (earth (ship-x) (ship-y))))
		(at start (not (ship-fly)))
		(at start (not (invasion-started)))
		(at start (p1))
	)
	:effect (and
		(increase (ship-x) (* 1 (vx-ship) #t))
		(increase (ship-y) (* 1 (vy-ship) #t))
		(at start (ship-fly))
		(at end (not (ship-fly)))
		(at start (invasion-started))
	)
)
(:durative-action bomb-rome1_101
	:parameters ()
	:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
	:condition (and
		(at start (not (drone1-busy)))
		(at end (drone1-busy))
		(at start (drone1-fly))
		(at end (drone1-fly))
		(over all (drone1-fly))
		(at start (not (rome-bombed)))
		(over all (inside (rome-region (drone1-x) (drone1-y))))
		(over all (invasion-ongoing))
	)
	:effect (and
		(at start (drone1-busy))
		(at end (not (drone1-busy)))
		(at end (rome-bombed))
		(at start (p1))
	)
)
(:durative-action bomb-london1_101
	:parameters ()
	:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
	:condition (and
		(at start (not (drone1-busy)))
		(at end (drone1-busy))
		(over all (invasion-ongoing))
		(at start (drone1-fly))
		(at end (drone1-fly))
		(over all (drone1-fly))
		(at start (not (london-bombed)))
		(over all (inside (london-region (drone1-x) (drone1-y))))
		(over all (invasion-ongoing))
	)
	:effect (and
		(at start (drone1-busy))
		(at end (not (drone1-busy)))
		(at end (london-bombed))
		(at start (p1))
	)
)
(:durative-action undock-drone1_101
	:parameters ()
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
		(increase (drone1-x) (* 1 (warp-speed) #t))
		(increase (drone1-y) (* 1 (warp-speed) #t))
		(at start (p1))
	)
)
(:durative-action bomb-paris1_101
	:parameters ()
	:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
	:condition (and
		(at start (not (drone1-busy)))
		(at end (drone1-busy))
		(at start (drone1-fly))
		(at end (drone1-fly))
		(over all (drone1-fly))
		(at start (not (paris-bombed)))
		(over all (inside (paris-region (drone1-x) (drone1-y))))
		(over all (invasion-ongoing))
	)
	:effect (and
		(at start (drone1-busy))
		(at end (not (drone1-busy)))
		(at end (paris-bombed))
		(at start (p1))
	)
)
(:durative-action fly-ship_121
	:parameters ()
	:duration (and (>= ?duration 0.1) (<= ?duration 200.0))
	:condition (and
		(over all (invasion-ongoing))
		(over all (inside (earth (ship-x) (ship-y))))
		(at start (not (ship-fly)))
		(at start (not (invasion-started)))
		(at start (not (p1)))
		(at start (not (p1_2)))
	)
	:effect (and
		(increase (ship-x) (* 1 (vx-ship) #t))
		(increase (ship-y) (* 1 (vy-ship) #t))
		(at start (ship-fly))
		(at end (not (ship-fly)))
		(at start (invasion-started))
		(at start (p1))
	)
)
(:durative-action bomb-ny2_101
	:parameters ()
	:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
	:condition (and
		(at start (not (drone2-busy)))
		(at end (drone2-busy))
		(at start (drone2-fly))
		(at end (drone2-fly))
		(over all (drone2-fly))
		(at start (not (ny-bombed)))
		(over all (inside (ny-region (drone2-x) (drone2-y))))
		(over all (invasion-ongoing))
	)
	:effect (and
		(at start (drone2-busy))
		(at end (not (drone2-busy)))
		(at end (ny-bombed))
		(at start (p1))
	)
)
(:durative-action undock-drone2_121
	:parameters ()
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
		(at start (not (p1)))
		(at start (not (p1_3)))
	)
	:effect (and
		(at start (drone2-undocking))
		(at end (not (drone2-undocking)))
		(at end (not (drone2-first-undock)))
		(increase (drone2-x) (* 1 (warp-speed) #t))
		(increase (drone2-y) (* 1 (warp-speed) #t))
		(at start (p1))
	)
)
(:durative-action fly-ship_141
	:parameters ()
	:duration (and (>= ?duration 0.1) (<= ?duration 200.0))
	:condition (and
		(over all (invasion-ongoing))
		(over all (inside (earth (ship-x) (ship-y))))
		(at start (not (ship-fly)))
		(at start (not (invasion-started)))
		(at start (not (p1)))
		(at end (not (p1)))
		(at start (p1_2))
		(at end (not (p1_9)))
	)
	:effect (and
		(increase (ship-x) (* 1 (vx-ship) #t))
		(increase (ship-y) (* 1 (vy-ship) #t))
		(at start (ship-fly))
		(at end (not (ship-fly)))
		(at start (invasion-started))
		(at start (not (p1_2)))
		(at start (p1_3))
		(at end (p1))
	)
)
(:durative-action bomb-london2_121
	:parameters ()
	:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
	:condition (and
		(at start (not (drone2-busy)))
		(at end (drone2-busy))
		(at start (drone2-fly))
		(at end (drone2-fly))
		(over all (drone2-fly))
		(at start (not (london-bombed)))
		(over all (inside (london-region (drone2-x) (drone2-y))))
		(over all (invasion-ongoing))
		(at start (not (p1)))
		(at start (not (p1_6)))
	)
	:effect (and
		(at start (drone2-busy))
		(at end (not (drone2-busy)))
		(at end (london-bombed))
		(at start (p1))
	)
)
(:durative-action undock-drone2_131
	:parameters ()
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
		(at start (not (p1)))
		(at end (p1))
		(at start (p1_3))
	)
	:effect (and
		(at start (drone2-undocking))
		(at end (not (drone2-undocking)))
		(at end (not (drone2-first-undock)))
		(increase (drone2-x) (* 1 (warp-speed) #t))
		(increase (drone2-y) (* 1 (warp-speed) #t))
		(at start (not (p1_3)))
		(at start (p1_4))
	)
)
(:durative-action start-invasion_151
	:parameters ()
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
		(at start (not (p1)))
		(at end (not (p1)))
		(at start (p1_0))
		(at end (p1_1))
	)
	:effect (and
		(at start (not (first-time)))
		(at end (invasion-ongoing))
		(at start (not (p1_0)))
		(at start (p1_1))
		(at end (not (p1_1)))
		(at end (p1_2))
	)
)
(:durative-action fly-drone2_141
	:parameters ()
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
		(at end (not (drone2-busy)))
		(at start (not (p1)))
		(at end (not (p1)))
		(at start (p1_4))
		(at end (not (p1_8)))
	)
	:effect (and
		(at start (drone2-fly))
		(at end (not (drone2-fly)))
		(increase (drone2-x) (* 1 (vx-drone2) #t))
		(increase (drone2-y) (* 1 (vy-drone2) #t))
		(at start (not (p1_4)))
		(at start (p1_5))
		(at end (p1))
	)
)
(:durative-action bomb-london2_141
	:parameters ()
	:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
	:condition (and
		(at start (not (drone2-busy)))
		(at end (drone2-busy))
		(at start (drone2-fly))
		(at end (drone2-fly))
		(over all (drone2-fly))
		(at start (not (london-bombed)))
		(over all (inside (london-region (drone2-x) (drone2-y))))
		(over all (invasion-ongoing))
		(at start (not (p1)))
		(at end (not (p1)))
		(at start (p1_6))
		(at end (not (p1_7)))
	)
	:effect (and
		(at start (drone2-busy))
		(at end (not (drone2-busy)))
		(at end (london-bombed))
		(at start (not (p1_6)))
		(at start (p1_7))
		(at end (p1))
	)
)
(:durative-action bomb-sf1_101
	:parameters ()
	:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
	:condition (and
		(at start (not (drone1-busy)))
		(at end (drone1-busy))
		(at start (drone1-fly))
		(at end (drone1-fly))
		(over all (drone1-fly))
		(at start (not (sf-bombed)))
		(over all (inside (sf-region (drone1-x) (drone1-y))))
		(over all (invasion-ongoing))
	)
	:effect (and
		(at start (drone1-busy))
		(at end (not (drone1-busy)))
		(at end (sf-bombed))
		(at start (p1))
	)
)
(:durative-action bomb-rome2_101
	:parameters ()
	:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
	:condition (and
		(at start (not (drone2-busy)))
		(at end (drone2-busy))
		(at start (drone2-fly))
		(at end (drone2-fly))
		(over all (drone2-fly))
		(at start (not (rome-bombed)))
		(over all (inside (rome-region (drone2-x) (drone2-y))))
		(over all (invasion-ongoing))
	)
	:effect (and
		(at start (drone2-busy))
		(at end (not (drone2-busy)))
		(at end (rome-bombed))
		(at start (p1))
	)
)
(:durative-action bomb-sf2_101
	:parameters ()
	:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
	:condition (and
		(at start (not (drone2-busy)))
		(at end (drone2-busy))
		(at start (drone2-fly))
		(at end (drone2-fly))
		(over all (drone2-fly))
		(at start (not (sf-bombed)))
		(over all (inside (sf-region (drone2-x) (drone2-y))))
		(over all (invasion-ongoing))
	)
	:effect (and
		(at start (drone2-busy))
		(at end (not (drone2-busy)))
		(at end (sf-bombed))
		(at start (p1))
	)
)
(:durative-action bomb-london2_131
	:parameters ()
	:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
	:condition (and
		(at start (not (drone2-busy)))
		(at end (drone2-busy))
		(at start (drone2-fly))
		(at end (drone2-fly))
		(over all (drone2-fly))
		(at start (not (london-bombed)))
		(over all (inside (london-region (drone2-x) (drone2-y))))
		(over all (invasion-ongoing))
		(at start (not (p1)))
		(at end (p1))
		(at start (p1_6))
	)
	:effect (and
		(at start (drone2-busy))
		(at end (not (drone2-busy)))
		(at end (london-bombed))
		(at start (not (p1_6)))
		(at start (p1_7))
	)
)
(:durative-action undock-drone2_141
	:parameters ()
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
		(at start (not (p1)))
		(at end (not (p1)))
		(at start (p1_3))
		(at end (not (p1_5)))
	)
	:effect (and
		(at start (drone2-undocking))
		(at end (not (drone2-undocking)))
		(at end (not (drone2-first-undock)))
		(increase (drone2-x) (* 1 (warp-speed) #t))
		(increase (drone2-y) (* 1 (warp-speed) #t))
		(at start (not (p1_3)))
		(at start (p1_4))
		(at end (p1))
	)
)
(:durative-action threat-whitehouse_101
	:parameters ()
	:duration (and (>= ?duration 0.1) (<= ?duration 0.1))
	:condition (and
		(over all (inside (wdc-region (ship-x) (ship-y))))
		(at start (london-bombed))
		(at start (paris-bombed))
		(at start (rome-bombed))
		(at start (ny-bombed))
		(at start (sf-bombed))
	)
	:effect (and
		(at end (not (invasion-ongoing)))
		(at end (above-whitehouse))
		(at start (p1))
	)
)
(:durative-action start-invasion_111
	:parameters ()
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
		(at start (p1))
	)
	:effect (and
		(at start (not (first-time)))
		(at end (invasion-ongoing))
	)
)
(:durative-action fly-drone1_101
	:parameters ()
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
		(at end (not (drone1-busy)))
	)
	:effect (and
		(at start (drone1-fly))
		(at end (not (drone1-fly)))
		(increase (drone1-x) (* 1 (vx-drone1) #t))
		(increase (drone1-y) (* 1 (vy-drone1) #t))
		(at start (p1))
	)
)
(:durative-action fly-drone2_111
	:parameters ()
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
		(at end (not (drone2-busy)))
		(at start (p1))
	)
	:effect (and
		(at start (drone2-fly))
		(at end (not (drone2-fly)))
		(increase (drone2-x) (* 1 (vx-drone2) #t))
		(increase (drone2-y) (* 1 (vy-drone2) #t))
	)
)
)