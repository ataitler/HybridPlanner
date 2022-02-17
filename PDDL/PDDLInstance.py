import re
from PDDL.PDDLSTypes import *


class PDDLSInstance(PDDLElement):
    elements = {}
    def __init__(self, name):
        PDDLElement.__init__(self, name)
        self.elements["name"] = name

    def AddRequirements(self, req):
        self.elements["requirements"] = req

    def GetRequirements(self):
        return self.elements["requirements"]

    def AddPredicates(self, preds):
        self.elements["predicates"] = preds

    def GetPredicates(self):
        return self.elements["predicates"]

    def AddFunctions(self, funcs):
        self.elements["functions"] = funcs

    def GetFunctions(self):
        return self.elements["functions"]

    def AddControlVariables(self, contvars):
        self.elements["control_variables"] = contvars

    def GetControlVariables(self):
        return self.elements["control_variables"]

    def AddControlVariablesDerivative(self, contvarsder):
        self.elements["control_variables_derivative"] = contvarsder

    def GetControlVariablesDerivative(self):
        return self.elements["control_variables_derivative"]

    def AddControlVariableVectors(self, vecs):
        self.elements["control_variable_vectors"] = vecs

    def GetControlVariableVectors(self):
        return self.elements["control_variable_vectors"]

    def AddSystems(self, systems):
        self.elements["systems"] = systems

    def GetSystems(self):
        return self.elements["systems"]

    def AddRegions(self, regions):
        self.elements["regions"] = regions
        return

    def GetRegions(self):
        return self.elements["regions"]

    def AddPhysicals(self, phys):
        self.elements["physicals"] = phys
        return

    def GetPhysicals(self):
        return self.elements["physicals"]

    def AddActivities(self, acts):
        self.elements["activities"] = acts

    def GetActivities(self):
        return self.elements["activities"]

    def AddInitState(self, initState):
        self.elements["init"] = initState

    def GetInitState(self):
        return self.elements["init"]

    def AddGoalSet(self, goalSet):
        self.elements["goal"] = goalSet

    def GetGoalSet(self):
        return self.elements["goal"]

    def AddMetric(self, metric):
        self.elements["metric"] = metric

    def GetMetric(self):
        return self.elements["metric"]

    def GenerateDomainFile(self, isPDDLS=0, domainFileName=None):
        # generate name
        domainTxt = "(define (domain " + self.elements["name"] + ")\n"

        # generate requirements
        domainTxt = domainTxt + "(" + self.elements["requirements"] + ")\n\n"

        # generate predicates
        domainTxt = domainTxt + "(:predicates\n"
        for _, pred in self.elements["predicates"].items():
            domainTxt = domainTxt + "\t(" + str(pred) + ")\n"

        # generate functions
        domainTxt = domainTxt + ")\n\n(:functions\n"
        for _, func in self.elements["functions"].items():
            domainTxt = domainTxt + "\t(" + str(func) + ")\n"
        domainTxt = domainTxt + ")\n\n"

        # generate control variables
        for _, contVar in self.elements["control_variables"].items():
            domainTxt = domainTxt + contVar.ToPDDL() + "\n"
        domainTxt = domainTxt + "\n"

        # generate control variable vectors
        for _, contVarVec in self.elements["control_variable_vectors"].items():
            domainTxt = domainTxt + contVarVec.ToPDDL() + "\n"
        domainTxt = domainTxt + "\n"

        # generate systems
        if isPDDLS == 0:
            for _, sys in self.elements["systems"].items():
                domainTxt = domainTxt + sys.ToPDDL() + "\n"
            domainTxt = domainTxt + "\n"

        # generate regions
        for _, region in self.elements["regions"].items():
            domainTxt = domainTxt + region.ToPDDL() + "\n"
        domainTxt = domainTxt + "\n"

        # generate physicals
        if isPDDLS == 0:
            for _, phy in self.elements["physicals"].items():
                domainTxt = domainTxt + phy.ToPDDL() + "\n"
            domainTxt = domainTxt + "\n"

        # generate activities
        for _, activity in self.elements["activities"].items():
            domainTxt = domainTxt + activity.ToPDDL() + "\n"
        domainTxt = domainTxt + ")"

        if domainFileName:
            f = open(domainFileName, 'w')
            f.write(domainTxt)
            f.close()

        return domainTxt


    def GenerateProblemFile(self, problemFileName=None):
        # generate name
        problemTxt = "(define (problem " + self.elements["name"] + "1)\n"
        problemTxt = problemTxt + "\t(:domain " + self.elements["name"] + ")\n"

        # generate init state
        problemTxt = problemTxt + "\t(:init\n"
        for _, initcond in self.elements["init"].items():
            problemTxt = problemTxt + "\t\t(" + initcond.ToPDDL() + ")\n"
        problemTxt = problemTxt + "\t)\n"

        # generate goal set
        problemTxt = problemTxt + "\t(:goal (and\n"
        for _, goalcond in self.elements["goal"].items():
            problemTxt = problemTxt + "\t\t(" + goalcond.ToPDDL() + ")\n"
        problemTxt = problemTxt + "\t)\n)\n)\n"

        # generate matric
        problemTxt = problemTxt + "(:metric minimize (+\n"
        for _, metric in self.elements["metric"].items():
            # print (metric)
            problemTxt = problemTxt + "\t\t" + metric.ToPDDL() + "\n"
        problemTxt = problemTxt + ")\n)\n"

        if problemFileName:
            f = open(problemFileName, 'w')
            f.write(problemTxt)
            f.close()

        return problemTxt


    def __str__(self):
        return self.name