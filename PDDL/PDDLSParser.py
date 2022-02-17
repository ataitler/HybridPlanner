import re
from PDDL.PDDLSTypes import *
from PDDL.PDDLInstance import *


class PDDLSParser():
	def __init__(self, domainFile, problemFile):
		self.domainFile = domainFile
		self.problemFile = problemFile
		self.PlanningInstance = None

	def GetParsedInstance(self):
		fh = open(self.domainFile, "r")
		domainTxt = fh.read()
		domainTxt = domainTxt.lower() + "\n\n"
		fh.close()
		domainTxt = self.__RemoveComments(domainTxt)

		name = self.__ParseName(domainTxt)

		# initialize the planning problem instance
		self.PlanningInstance = PDDLSInstance(name)

		# add the requirements of the pddl domain
		reqs = self.__ParseRequirements(domainTxt)
		self.PlanningInstance.AddRequirements(reqs)

		# add the predicates of the pddl domain
		predicates = self.__ParsePredicates(domainTxt)
		self.PlanningInstance.AddPredicates(predicates)

		# add the functions of the pddl domain
		functions = self.__ParseFunctions(domainTxt)
		self.PlanningInstance.AddFunctions(functions)

		# add the control variables of the pddl domain
		controlVars = self.__ParseControlVariables(domainTxt)
		self.PlanningInstance.AddControlVariables(controlVars)

		controlVarsDerivatives = self.__ParseControlVariablesDerivatives(domainTxt, controlVars)
		self.PlanningInstance.AddControlVariablesDerivative(controlVarsDerivatives)

		# add the control variables vector of the pddl domain
		controlVarVectors = self.__ParseControlVariablesVectors(domainTxt,controlVars)
		self.PlanningInstance.AddControlVariableVectors(controlVarVectors)

		# add the system definitions of the pddl domain
		systems = self.__ParseSystems(domainTxt, controlVars, functions, controlVarsDerivatives)
		self.PlanningInstance.AddSystems(systems)

		# add the regions of the pddl domain
		regions = self.__ParseUngroundedRegions(domainTxt)
		self.PlanningInstance.AddRegions(regions)

		# add the physical definitions of the pddl domain
		physicals = self.__ParsePhysicals(domainTxt, regions)
		self.PlanningInstance.AddPhysicals(physicals)

		# add the possible activities in the pddl domain
		activities = self.__ParseActivities(domainTxt, predicates, regions, functions, controlVars, controlVarVectors, systems)
		self.PlanningInstance.AddActivities(activities)

		# add initial state
		fh = open(self.problemFile, "r")
		problemTxt = fh.read()
		problemTxt = problemTxt.lower()
		fh.close()
		problemTxt = self.__RemoveComments(problemTxt)
		initState = self.__ParseInitState(problemTxt, functions, predicates)
		self.PlanningInstance.AddInitState(initState)

		goalSet = self.__ParseGoalSet(problemTxt, predicates)
		self.PlanningInstance.AddGoalSet(goalSet)

		metric = self.__ParseMetric(problemTxt)
		self.PlanningInstance.AddMetric(metric)

		return self.PlanningInstance

	def __RemoveComments(self, txt):
		txt = re.sub("(?m)^\s*;.*?\n", "\n", txt)
		return txt

	def __ParseName(self, domTxt):
		m = re.search("\(define\s?\(domain\s(\S+?)\)", domTxt)
		return m.group(1)

	def __ParseRequirements(self, domTxt):
		m = re.search("\((:requirements.*)\)", domTxt)
		if m is None:
			return None
		return m.group(1)

	def __ParsePredicates(self, domTxt):
		preds = {}
		m = re.search("\(:predicates\s+(\S+\s+)*?\)", domTxt).group(0)
		if m is None:
			return None
		m = re.search("(?s)\(:predicates.*?(\S+.*)\)", m).group(0)
		m = re.search("(?s)\((\S+)\)(.*)", m)
		while m is not None:
			predName = m.group(1)
			p = Predicate(predName)
			preds[predName] = p
			m = m.group(2)
			m = re.search("(?s)\((\S+)\)(.*)", m)
		return preds

	def __ParseFunctions(self, domTxt):
		funcs = {}
		m = re.search("\(:functions\s+(\S+\s+)*?\)", domTxt).group(0)
		if m is None:
			return None
		m = re.search("(?s)\(:functions.*?(\S+.*)\)", m).group(0)
		m = re.search("(?s)\((\S+)\)(.*)", m)
		while m is not None:
			funcName = m.group(1)
			f = Function(funcName)
			funcs[funcName] = f
			m = m.group(2)
			m = re.search("(?s)\((\S+)\)(.*)", m)
		return funcs

	def __ParseControlVariables(self, domTxt):
		contvars = {}
		m = re.findall("(?s)\(:control-variable\s.*?\s*?:bounds.*?\n", domTxt)
		for match in m:
			m_c = re.search("(?s)\(:control-variable\s(.*?)\s*?:bounds.*", match)
			name = m_c.group(1)
			m_c = re.search("bounds\s?\(and\s?\(>=\s?\?value\s?([-]?\d+[.]?\d*?)\)\s*\(<=\s?\?value\s?([-]?\d+[.]?\d*?)\)\)", match)
			lb = float(m_c.group(1))
			ub = float(m_c.group(2))
			c = ControlVariable(name, lb, ub)
			contvars[name] = c
		return contvars

	def __ParseControlVariablesDerivatives(self, domTxt, controlVariables):
		derscont = {}
		dersacc = {}
		ders = {}
		m = re.findall("(?s)\(:control-variable-derivative\s*(.*?)\s*:control-variable\s*(.*?)\s*:bounds\s*"
					   "\(\s*and\s*\(\s*>=\s*\?value\s*([-]?\d+[.,]?\d*)\)\s*\(\s*<=\s*\?value\s*([-]?\d+[.,]?\d*)\s*"
					   "\)\s*\)\s*\)", domTxt)
		for match in m:
			name = match[0]
			controlVarName = match[1]
			lb = float(match[2])
			ub = float(match[3])
			if controlVarName not in controlVariables.keys():
				raise ValueError("Unrecognied derivative in control variables derivative parser: no such control variable")
			controlVar = controlVariables[controlVarName]
			contDer = ControlVariableDerivative(name, lb, ub, controlVar)
			dersacc[name] = contDer
			derscont[controlVarName] = contDer
		ders["by-controls"] = derscont
		ders["by-derivatives"] = dersacc
		return ders

	def __ParseControlVariablesVectors(self, domTxt, controlVariables):
		vects = {}
		m = re.findall("(?s)\(:control-variable-vector.*?:control-variables.*?:max-norm.*?\)", domTxt)
		for match in m:
			m_v = re.search("(?s)\(:control-variable-vector\s*(.*?)\s*:control-variables\s*\(\((.*?)\)\s*\((.*?)\)\).*?:max-norm\s*(\d+[.,]?\d*)\s*\)",match)
			name = m_v.group(1)
			try:
				contvar1 = controlVariables[m_v.group(2)]
				contvar2 = controlVariables[m_v.group(3)]
			except:
				raise ValueError("Undeclered control variables in control-variable-vector parser.")
			v = ControlVariableVector(name, contvar1, contvar2, float(m_v.group(4)))
			vects[name] = v
		return vects

	def __ParseSystems(self, domTxt, controlVariables, functions, controlDerivatives):
		systems = {}
		m = re.findall("(?s)\(:system.*?:input.*?:output.*?:battery.*?:parameters.*?\)\).*?\)", domTxt)
		for match in m:
			m_s = re.search("(?s)\(:system\s*(.*?)\s*:input\s*\(\((.*?)\)\s*\((.*?)\)\)\s*:output\s*\(\((.*?)\)\s*" \
							"\((.*?)\)\)\s*:battery\s*\(\s*(.*?)\s*\)\s*:parameters\s*\((\(.*?\s*\))\s*\)\s*\)", match)
			name = m_s.group(1)
			controlX = m_s.group(2)
			controlY = m_s.group(3)
			stateX = m_s.group(4)
			stateY = m_s.group(5)
			battery = m_s.group(6)
			param_str = re.findall("(?s)\((\d[,.]?\d*)\)", m_s.group(7))
			param = []
			for p in param_str:
				param.append(float(p))
			try:
				controlX = controlVariables[controlX]
				controlY = controlVariables[controlY]
				stateX = functions[stateX]
				stateY = functions[stateY]
				if not battery:
					battery = None
				else:
					battery = functions[battery]
			except:
				raise ValueError("Undeclereed control variables or functions in system parser")
			s = System(name, [stateX, stateY], [controlX, controlY], battery, param)
			try:
				s.SetAcceleration(controlDerivatives["by-controls"][str(controlX)])
				s.SetAcceleration(controlDerivatives["by-controls"][str(controlY)])
			except Exception as inst:
				raise inst
			systems[name] = s
		return systems

	def __ParseUngroundedRegions(self, domTxt):
		regions = {}
		m = re.findall("(?s)\(:region\s*.*?\s*:parameters\s*\(.*?\)\s*:condition\s*.*?\)\s*\)\s*\)\s*?\n", domTxt)
		for region in m:
			m_r = re.search("(?s)\(:region\s*(.*?)\s*:parameters\s*\((.*?)\)\s*:condition\s*(.*?\)\s*\))\s*\)\s*?\n", region)
			name = m_r.group(1)
			params = re.findall("\?(\S+)", m_r.group(2))
			condtype = re.search("\(and\s*\((\S+)", m_r.group(3)).group(1)
			cond = re.search("(?s)\(and\s*(.*)\)", m_r.group(3)).group(1)
			reg = None
			if condtype == "in-rect":
				# Parse rectangular conditions
				parsedConditions = self.__ParseRectRegion(cond)
				reg = RectRegion(name, params, parsedConditions[0], parsedConditions[1], parsedConditions[2])
			elif condtype == "in-poly":
				# Parse polygonal conditions
				vertices = self.__ParsePolyRegion(cond)
				reg = PolyRegion(name, params, vertices)
			elif condtype == "in-circle":
				# Parse circular conditions
				parsedConditions = self.__ParseCircRegion(cond)
				reg = CircleRegion(name, params, parsedConditions[0], parsedConditions[1])
			elif condtype == "max-distance":
				# Parse max-distance conditions
				dist = self.__ParseDistRegion(cond)
				reg = DistRegion(name, params, dist)
			elif condtype == "<=":
				# Parse polygonal conditions
				inqs = self.__ParseConvRegion(cond)
				reg = ConvRegion(name, params, inqs)
			else:
				raise ValueError("Unrecognized region type in region parser")
			regions[name] = reg
		return regions

	def __ParseRectRegion(self, condition):
		m = re.search("(?s)\(\S+\s*\((.*?)\)\s*:corner\s*\((.*?)\)\s*:width\s*(\d+[.]?\d*)\s*:height\s*(\d+[.]?\d*)\)", condition)
		corner = re.findall("(\d+[.]?\d*)", m.group(2))
		width = m.group(3)
		height = m.group(4)
		return [corner, width, height]

	def __ParsePolyRegion(self, condition):
		m = re.search("(?s)\(\S+\s*\((.*?)\)\s*:vertices\s*(.*)\)", condition)
		vertices = re.search("\((.*)\)", m.group(2)).group(1)
		vertices = re.findall("\((\d+[.]?\d*)\s*(\d+[.]?\d*)\)", vertices)
		return vertices

	def __ParseCircRegion(self, condition):
		m = re.search("(?s)\(\S+\s*\((.*?)\)\s*:center\s*(.*?)\s*:r\s*(.*)\)", condition)
		center = re.findall("(\d+[.]?\d*)", m.group(2))
		radius = re.search("(\d+[.]?\d*)", m.group(3)).group(1)
		return [center, radius]

	def __ParseDistRegion(self, condition):
		m = re.search("(?s)\(\S+\s*\((.*)\)\s*:d\s*(.*)\)", condition)
		dist = m.group(2)
		return dist

	def __ParseConvRegion(self, condition):
		inequalities = []
		m = re.findall("([<>=]=?)\s*(.*?)\s*(\d+[.]\d*)\)", condition)
		for convCond in m:
			ineqType = convCond[0]
			b = convCond[2]
			m1 = re.search("\(([+-])\s*(.*)\)", convCond[1])
			connect = m1.group(1)
			a = re.findall("\(([*\/])\s*([-]?\d+[.]\d*)\s*\(([-+])\s*\?(\S+)\s*\?(\S+)\)\)", m1.group(2))
			inequalities.append([ineqType, a, connect, b])
		return inequalities

	def __ParsePhysicals(self, domTxt, regionsDic):
		phys = {}
		m = re.findall("(?s)\(:physical\s*.*?\s*:regions\s*\(.*?\)\s*:parameters\s*\(.*?\)\s*\)", domTxt)
		for physical in m:
			m_p = re.search("(?s)\(:physical\s*(.*?)\s*:regions\s*\((.*?)\)\s*:parameters\s*\((.*?)\)\s*\)", physical)
			name = m_p.group(1)
			param = float(m_p.group(3))
			regions = m_p.group(2)
			regionsList = re.findall("\(.*?\)", regions)
			regionsNum = len(regionsList)
			if regionsNum >= 1:
				for i in xrange(regionsNum):
					itername = name + str(i+1)
					regionName = re.search("\((.*?)\)",regionsList[i]).group(1)
					# check region is a recognized region
					if regionName in regionsDic:
						p = Physical(itername, regionName, param)
					else:
						raise ValueError("Physical definition for undeclared region found in physical parser")
					#check region is not in physical dictionary
					if regionName not in phys:
						phys[regionName] = p
					else:
						raise ValueError("Ambiguity in physical declaration in physical parser")
			else:
				# handle the default region
				regionName = "default"
				if regionName in phys:
					raise ValueError("Ambiguous declaration of default physical in physical parser")
				else:
					p = Physical(name, "", param)
					phys[regionName] = p
		if len(phys) == 0:
			p = Physical("default", "", 0.05)
			phys["default"] = p
		return phys

	def __ParseActivities(self, domTxt, predicates, regions, functions, controls, controlVecs, systems):
		act = {}
		actions = self.__ParseUngroundedActions(domTxt, predicates)
		duractions = self.__ParseUngroundedDurativeActions(domTxt, predicates, regions, functions, controls, controlVecs, systems)
		allActivities = actions + duractions
		for activity in allActivities:
			act[activity.name] = activity
		return act

	def __ParseUngroundedActions(self, domTxt, predicates):
		actions = []
		m = re.findall("(?s):action\s*.*?\s*:parameters\s*\(.*?\)\s*:precondition\s*\(and\s*.*?\s*\)\s*:effect\s*\(and\s*.*?\)\s*\)\s*\)\n[\n\(]", domTxt)
		for a in m:
			m_a = re.search("(?s):action\s*(.*?)\s*:parameters\s*\((.*?)\)\s*:precondition\s*\(and\s*(.*?)\s*\)\s*:effect\s*\(and\s*(.*?\))\s*\)\s*\)\n[\n\(]", a)
			name = m_a.group(1)
			params = m_a.group(2)
			precond = m_a.group(3)
			eff = m_a.group(4)

			# parse parameters
			if params == "":
				params = []
			else:
				params = re.findall("(?s)\?(\w*)", params)

			# TODO: fix grounding prameters in conditions and effect (not just specific predicates)

			# parse preconditions
			literals = re.findall("(?s)\((.*?)\)\s*(\n|$)", precond)
			preconds = []
			for lit in literals:
				lit0 = lit[0]
				isNot = re.search("not\s*\((.*?)\)", lit0)
				if isNot is None:
					try:
						pred = ConditionalPredicate(predicates[lit0], True)
					except:
						raise ValueError("Unrecognized predicate " + lit0 +"in action parser")
				else:
					pred = ConditionalPredicate(predicates[isNot.group(1)], False)
				preconds.append(pred)

			# parse effects
			literals = re.findall("(?s)\((.*?)\)\s*(\n|$)", precond)
			effs = []
			for lit in literals:
				lit0 = lit[0]
				isNot = re.search("not\s*\((.*?)\)", lit0)
				if isNot is None:
					try:
						pred = ConditionalPredicate(predicates[lit0], True)
					except:
						raise ValueError("Unrecognized predicate " + lit0 + " in action parser")
				else:
					pred = ConditionalPredicate(predicates[isNot.group(1)], False)
				effs.append(pred)

			a = Action(name, params, preconds, effs)
			actions.append(a)
		return actions

	def __ParseUngroundedDurativeActions(self, domTxt, predicates, regions, functions, controls, controlsVecs, systems):
		duractions = []
		# remove headers first
		domTxt = re.search("(?s)\(define.*?\)\s*\(:requirements.*?\)\s*(.*)", domTxt).group(1)
		m = re.findall("(?s):durative-action\s*.*?\s*:duration\s*.*?:condition\s*\(and\s*.*?\s*\)\s*:effect\s*\(and\s*.*?\)\s*\)\s*\)\n[\n\(]", domTxt)
		for daction in m:
			m_d = re.search("(?s):durative-action\s*(.*?)\s*:duration\s*(.*?):condition\s*\(and\s*(.*?)\s*\)\s*:effect\s*\(and\s*(.*?\))\s*\)\s*\)\n[\n\(]", daction)
			name = m_d.group(1)
			params = []
			durations = m_d.group(2)
			cond = m_d.group(3)
			eff = m_d.group(4)

			# parse name and parameters
			m_param = re.search("\s*(.*?)\s*:parameters\s*\((.*?)\)\s*", name)
			if m_param is not None:
				name = m_param.group(1)
				params = m_param.group(2)
				params = re.findall("(?s)\?(\w*)", params)

			# parse durations
			m_dur = re.search("(?s)\(and\s*\(\>\=\s*\?duration\s*(\d*[.,]?\d*?)\)\s*\(\<\=\s*\?duration\s*(\d*[.,]?\d*?)\)\)", durations)
			dur_lb = m_dur.group(1)
			dur_ub = m_dur.group(2)

			# parse conditions
			parsedConditions = []
			conds = re.findall("(?s)\((.*?)\)\s*(\n|$)", cond)
			for cond,_ in conds:
				parsedCondition = self.__ParseDurativeConditionsEffects(cond, predicates, regions, functions, None, None)
				parsedConditions.append(parsedCondition)

			# parse effects
			parsedEffects = []
			numericEffects = []
			effs = re.findall("(?s)\((.*?)\)\s*(\n|$)", eff)
			for eff,_ in effs:
				parsedEffect = self.__ParseDurativeConditionsEffects(eff, predicates, regions, functions, controls, controlsVecs)
				parsedEffects.append(parsedEffect)
				if isinstance(parsedEffect, NumericEffect):
					numericEffects.append(parsedEffect)
				if isinstance(parsedEffect, TimedGroundedRegion):
					reg = parsedEffect.Region
				else:
					reg = None

			master_systems, slave_systems = self.__InferSystemFromNumericEffects(numericEffects, systems)

			action = DurativeAction(name, params, [dur_lb, dur_ub], parsedConditions, parsedEffects, reg)
			action.SetSystems(master_systems, slave_systems)
			duractions.append(action)
		return duractions

	def __ParseDurativeConditionsEffects(self, expr, predicates, regions, functions, controls, controlVecs):
		singleCond = re.search("(?s)(\w+\s\w+)\s*\((.*)\)", expr)
		# numeric effect
		if singleCond is None:
			numericE = re.search("(?s)(\w{3}rease)\s*\((\S*)\)\s*\(([\*\\+-])\s*(\d+[.,]?\d*)?\s*\((.*?)\)\s*#t\)", expr)
			# print (expr)
			incdec = numericE.group(1)
			state = numericE.group(2)
			input = numericE.group(5)
			op = numericE.group(3)
			coeff = numericE.group(4)
			norm = None
			if coeff is None:
				coeff = "1"
			m_n = re.search("(?s)(\S*)\s*\((\S*)\)", input)
			if m_n is not None:
				norm = m_n.group(1)
				input = m_n.group(2)
				cont = controlVecs[input]
			else:
				cont = controls[input]
			try:
				parsedCondition = NumericEffect(incdec, functions[state], op, cont, norm, coeff)
			except:
				raise ValueError("Unable to parse numeric effect in durative action prasing")
			return parsedCondition

		timedDescriptor = singleCond.group(1)
		rest = singleCond.group(2)
		# regular negative predicate
		isNot = re.search("(?s)\s*not\s\((.*?)\s*\)", rest)
		if isNot != None:
			pred = isNot.group(1)
			if pred not in predicates:
				raise ValueError("Unrecognized predicate " + pred + " in durative action parsing")
			else:
				parsedCondition = TimedConditionalPredicate(predicates[pred], timedDescriptor,False)
		else:
			# predicate
			isPredicate = re.search("(?s)^\s*(\S*)\s*$", rest)
			isFunction = re.search("(?s)([><=]{1,2})\s*\((\S*)\)\s*(\d+[,.]?\d*)", rest)
			isRegion = re.search("(?s)inside\s*\((\S*)\s*\s*\((\S*)\)\s*\((\S*)\)\s*?\)", rest)
			isDist = re.search("(?s)inside\s*\((\S*)\s*\s*\((\S*)\)\s*\((\S*)\)\s*\((\S*)\)\s*\((\S*)\)\s*?\)", rest)
			# predicate
			if isPredicate is not None:
				pred = isPredicate.group(1)
				try:
					parsedCondition = TimedConditionalPredicate(predicates[pred], timedDescriptor, True)
				except:
					raise ValueError("Unrecognized predicate " + pred + " in durative action parsing: " + singleCond.group(0))
			# function
			elif isFunction is not None:
				try:
					func = functions[isFunction.group(2)]
				except:
					raise ValueError("Unrecognized function " + isFunction.group(2) + " in durative action parsing")
				parsedCondition = TimedInitializedFunction(func, isFunction.group(1), isFunction.group(3), timedDescriptor)
			# region
			elif isRegion is not None:
				region = isRegion.group(1)
				state1 = isRegion.group(2)
				state2 = isRegion.group(3)
				try:
					region = regions[region]
					region = region.GetGrounded([functions[state1], functions[state2]])
				except:
					raise ValueError("Unable to ground region " + region + " in durative action parsing")
				parsedCondition = TimedGroundedRegion(region, timedDescriptor)
			# max distance region
			elif isDist is not None:
				region = isDist.group(1)
				state1 = isDist.group(2)
				state2 = isDist.group(3)
				state3 = isDist.group(4)
				state4 = isDist.group(5)
				try:
					region = regions[region]
					region = region.GetGrounded([functions[state1], functions[state2], functions[state3], functions[state4]])
				except:
					raise ValueError("Unable to ground region " + region + " in durative action parsing")
				parsedCondition = TimedGroundedRegion(region, timedDescriptor)
			else:
				raise ValueError("Unrecognized condition: " + expr)
		return parsedCondition

	def __InferSystemFromNumericEffects(self, numericEffects, systems):
		master_systems = []
		slave_systems = []
		for numEff in numericEffects:
			func = numEff.Output
			cont = numEff.Input
			# only movement (increase effects)
			if numEff.IncDec == "increase":
				# look for master systems
				for sys in systems.keys():
					if systems[sys].isState(func):
						if systems[sys].isControl(cont):
							if systems[sys] not in master_systems:
								master_systems.append(systems[sys])
						break
				# look for slave systems
				for sys in systems.keys():
					if systems[sys].isState(func):
						if not systems[sys].isControl(cont):
							for master in master_systems:
								if master.isControl(cont):
									if systems[sys] not in slave_systems:
										slave_systems.append(systems[sys])
								break
			# battery is ignored at this stage
		return master_systems, slave_systems

	def __ParseInitState(self ,probTxt, functions, predicates):
		initF = {}
		m = re.search("(?s)\(:init\s*(.*?)\s*\)\s*\(:goal", probTxt)
		initFunctions = re.findall("(?s)\(\s*=\s*\(.*?\)\s*\d+[.,]?\d*\s*\)", m.group(1))
		f = re.compile("(?s)\(\s*=\s*\(.*?\)\s*\d+[.,]?\d*\s*\)")
		b = f.sub("", m.group(1))
		initPredicates = re.findall("(?s)\(\s*?(\S*?)\s*?\)", b)

		for func in initFunctions:
			m_f = re.search("(?s)\(\s*=\s*\((.*?)\)\s*(\d+[.,]?\d*)\s*\)", func)
			f = m_f.group(1)
			val = m_f.group(2)
			try:
				af = AssignedFunction(f, functions[f], val)
			except:
				raise ValueError("error in function name, in init state parsing: no such function exist in domain")
			initF[f] = af

		for pred in initPredicates:
			try:
				initF[pred] = predicates[pred]
			except:
				raise ValueError("error in predicate name in init state parsing: no such predicate exist in domain")

		return initF

	# TODO: add support for numeric constraints
	def __ParseGoalSet(self, probTxt, predicates):
		goalF = {}
		notpreds = []
		m = re.search("(?s)\(:goal\s*?\(\s*?and\s*.*?\)\s*?\)\s*?\)\s*?\)", probTxt)

		# negative conditioned predicates
		preds = re.findall("(?s)\(not\s*\((\S*?)\)", m.group(0))
		for pred in preds:
			try:
				goalF[pred] = ConditionalPredicate(predicates[pred], False)
				notpreds.append(pred)
			except:
				raise ValueError("error in predicate name in goal set parsing, no such predicate exist in domain: " + pred)

		# positive conditioned predicates
		preds = re.findall("(?s)\((\S*?)\)", m.group(0))
		for pred in preds:
			try:
				if pred not in notpreds:
					goalF[pred] = ConditionalPredicate(predicates[pred], True)
			except:
				raise ValueError("error in predicate name in goal set parsing, no such predicate exist in domain")

		return goalF


	def __ParseMetric(self, probTxt):
		metricD = {}
		m = re.search("(?s)\(:metric\s*?minimize\s*?\(\+\s*?(\(.*)\)\s*?\)", probTxt).group(1)
		met = re.findall("(?s)\(\*\s*?(\-?\d+[,.]?\d*)\s*?\((\S*?)\)\s*?\)", m)
		for metric in met:
			metricD[metric[1]] = Metric(metric[1], metric[0])
		return metricD
