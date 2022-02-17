import sys
import subprocess
import os
from PDDL.PDDLSParser import *
from PDDL.PathEliminationCompilation import *
from PlanHandler.PlanUtils import *
from Graphics.AlienInvasionDomainVisualier import *
from Graphics.Plan2Vec import *


#constants
SCOTTY_DOMAIN_FILE = "Domains/scotty_domain"
SCOTTY_PROBLEM_FILE = "Domains/scotty_problem"
JSON_FILE = "plan.json"


def main():
    """main planning loop"""
    if len(sys.argv) < 3:
        print("Usage: AliensInvasion.py <domain> <problem> <k=1>")
        return

    # print (len(sys.argv))
    print("Hello and welcome to the alien invasion!")


    domainFile = sys.argv[1]
    problemFile = sys.argv[2]

    planCount = 1
    if len(sys.argv) > 3:
        planCount = int(sys.argv[3])

    eliminationMaps = []
    k = 0
    while k < planCount:

        print (domainFile, problemFile)
        p = PDDLSParser(domainFile+".pddl", problemFile+".pddl")
        PlanningInstance = p.GetParsedInstance()

        # generate clean PDDLS version of the PDDL files (no physicals or systems)
        Scottydomain = SCOTTY_DOMAIN_FILE+str(k)+".pddl"
        Scottyproblem = SCOTTY_PROBLEM_FILE+str(k)+".pddl"
        PlanningInstance.GenerateDomainFile(1, Scottydomain)
        PlanningInstance.GenerateProblemFile(Scottyproblem)

        # execute scotty
        # scottyCmd = ["../../../Planning/cqScotty2/scotty -o " + JSON_FILE + " --search-method astar " + SCOTTY_DOMAIN_FILE + " " + SCOTTY_PROBLEM_FILE]
        # scottyCmd = ["../../../Planning/cqScotty2/scotty", "-o", JSON_FILE, "--search-method", "astar", Scottydomain, Scottyproblem]
        # scottyCmd = "~/Planning/cqScotty2/scotty  "
        # os.system(scottyCmd)
        #with open(os.devnull, 'w') as devnull:
        #    subprocess.run(scottyCmd, stdout=devnull, stderr=subprocess.STDOUT)

        # sys.exit(0)

        # JSON_FILE = "plan_min_time.json"
        # JSON_FILE = "plan_min_time2.json"
        # JSON_FILE = "plan_min_time_energy.json"       # 60 fps
        JSON_FILE = "plan_min_time_energy_all.json" #7 0 fps

        planReader = PlanReader(JSON_FILE)
        plan = planReader.GetPlan()
        plan.MapInput2Sys(PlanningInstance.GetControlVariables(), PlanningInstance.GetSystems())

        # print ("long plan:")
        # print (plan.PrintPlan(eliminationMaps))
        print (plan.PrintSegments())

        #TODO: fix visualization of compiled plans
        planEvents = plan.GetEvents(eliminationMaps)
        # print (planEvents)
        # planEvents = plan.GetEvents()
        planVectorsGenerator = Plan2Vec(planEvents)
        # planVectorsGenerator = CSV2Vec("trajectories1000.csv")
        # print (planEvents)
        sys.exit(0)

        # visualize domain
        Aliens = AlienInvasionDomainVisulizer()
        ship = planVectorsGenerator.GetShipTrajectory()
        d1 = planVectorsGenerator.GetDrone1Trajectory()
        d2 = planVectorsGenerator.GetDrone2Trajectory()
        explosions = planVectorsGenerator.ExplosionsTiming()
        # print((d2))
        # sys.exit(0)


        Aliens.GameRollout(ship, d1, d2, explosions, True)


        # compile new domain
        planEvents = plan.GetEvents()
        planSeq = PlanSequence(planEvents)
        compiled = CompiledPlanningInstance(PlanningInstance, planSeq, k+1)
        eliminationMaps.insert(0, compiled.GetTansformation())
        compiled.Compile()
        domainFile = domainFile + str(k+1)
        problemFile = problemFile + str(k+1)
        compiled.GenerateCompiledDomainFile(domainFile+".pddl", 0)
        compiled.GenerateCompiledProblemFile(problemFile+".pddl")

        k = k + 1


if __name__ == "__main__":
    main()






