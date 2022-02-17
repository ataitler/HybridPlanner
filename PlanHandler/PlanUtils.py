import json
import copy
import math
import re
import copy

class PlanReader():
    def __init__(self, jsonPlanFile):
        with open(jsonPlanFile) as f:
            planData = json.load(f)
        self.plan = Plan(planData["plan"])

    def GetPlan(self):
        return self.plan


class Plan():
    def __init__(self, planData):
        self.events = {}
        self.segments = {}
        self.IC = {}
        self.input2sys = {}
        ind = 0

        self.objective = planData["objective"]
        self.steps = planData["num-steps"]
        self.makespan = planData["makespan"]

        if len(planData["steps"]) < 1:
            raise ValueError("No plan has been found")

        for key in planData["steps"][0]["control-variables-nextstage"].keys():
            self.IC[key.lower()] = 0.0

        for step in planData["steps"]:
            index = int(step["index"])
            relatedEvent = int(step["related-step-index"])
            activity = step["action"].lower()
            init_states = {}
            for key, val in step["state-variables"].items():
                init_states[key.lower()] = val
            controls = {}
            for key, val in step["control-variables-nextstage"].items():
                controls[key.lower()] = round(val, 3)
            startTime = round(float(step["step-time"])*1000)/1000.0

            if relatedEvent in self.events:
                isStart = False
                start_e = self.events[relatedEvent]
                s = Segment(ind, activity, start_e.StartTime, startTime, start_e.States, init_states, start_e.Controls, controls)
                self.segments[start_e.startTime] = s
                duration = startTime - start_e.StartTime
                ind = ind + 1
            else:
                isStart = True
                duration = round(float(step["duration"])*1000)/1000.0
            e = Event(index, startTime, duration, activity, isStart, init_states, controls, relatedEvent)
            self.events[index] = e
            self.activitiesNum = ind
            tempSeg = {}
            ind = 0
            for i in sorted(self.segments.keys()):
                tempSeg[ind] = self.segments[i]

    def __str__(self):
        return "plan"

    def MapInput2Sys(self, controlVars, systems):
        for func in self.IC.keys():
            if func in controlVars.keys():
                for sys in systems.keys():
                    if systems[sys].isControl(controlVars[func]):
                        self.input2sys[func] = sys

    def RevetToOriginalSpace(self, events, Map=[]):
        if len(Map) == 0:
            return events
        else:
            pattern = re.compile("(?s)(.*?\-)(.*)")
            for i in range(len(Map)):
                map = Map[i]
                for i in range(self.steps):
                    m = pattern.match(events[i].Name)
                    events[i].Name = m.group(1)+map[m.group(2)]
            return events



    def PrintPlan(self, Map=[]):
        st = ""
        localEvents = copy.deepcopy(self.events)
        localEvents = self.RevetToOriginalSpace(localEvents, Map)
        for i in range(self.steps):
            st = st + localEvents[i].ToString() + "\n\n"
        return st

    def PrintSegments(self):
        st = ""
        #for i in xrange(self.activitiesNum):
        for i in sorted(self.segments.keys()):
            st = st + self.segments[i].ToString() + "\n"
        return st

    @property
    def GetPlan(self):
        return self.segments

    def GetEvents(self, Map=[]):
        if len(Map) > 0:
            localEvents = copy.deepcopy(self.events)
            localEvents = self.RevetToOriginalSpace(localEvents, Map)
            # pattern = re.compile("(?s)(.*?\-)(.*)")
            # map = map[0]
            # for i in range(self.steps):
            #     m = pattern.match(localEvents[i].Name)
            #     localEvents[i].Name = m.group(1)+map[m.group(2)]
            return localEvents
        return self.events

    def GenerateControlSegments(self, activities, systems, physicals):
        controlSegements = []
        v0_prev = 0
        v0_next = 0
        vf = 0
        x0 = 0
        xf = 0
        T = 0
        alpha = 0.1
        k = 0.05

        prev_controls = copy.deepcopy(self.IC)
        t0 = 0
        for eventInd, event in self.events.iteritems():
            active_systems = []
            if event.Index == self.steps-1:
                continue

            # determine the active systems in the current event
            for input, value in event.Controls.iteritems():
                if value != 0:
                    s2c = self.input2sys[input]
                    if s2c not in active_systems:
                        active_systems.append(s2c)

            # infer initial and final condition for each system separately
            for sys in active_systems:
                x = systems[sys].GetState()["x"]
                y = systems[sys].GetState()["y"]
                ux = systems[sys].GetInputDerivatives()["x"]
                uy = systems[sys].GetInputDerivatives()["y"]
                vx = systems[sys].GetInput()["x"]
                vy = systems[sys].GetInput()["y"]

                # initial conditions
                x0 = round(event.States[str(x)], 3)
                y0 = round(event.States[str(y)], 3)
                vx0 = prev_controls[str(vx)]
                vy0 = prev_controls[str(vy)]
                X0 = [x0, vx0]
                Y0 = [y0, vy0]

                # final conditions
                xf = round(self.events[eventInd+1].states[str(x)], 3)
                yf = round(self.events[eventInd+1].states[str(y)], 3)
                vxf = event.Controls[str(vx)]
                vyf = event.Controls[str(vy)]
                Xf = [xf, vxf]
                Yf = [yf, vyf]

                # infer physical properties of the event
                if event.activity in activities.keys():
                    a = activities[event.activity]
                    r = a.Region
                    if r in physicals.keys():
                        k = float(physicals[r].param)
                    elif "default" in physicals.keys():
                        k = float(physicals["default"].param)
                    else:
                        k = 0.05

                # set the control segment for both axes
                segment = ControlSegment(sys, event.eventName, eventInd)
                segment.alpha = 0.1
                segment.k = k
                segment.m = float(systems[sys].param[0])
                segment.SetDuration(self.events[eventInd+1].StartTime - event.StartTime)
                segment.SetInitConditions(X0, Y0)
                segment.SetFinalConditions(Xf, Yf)
                segment.SetAccBounds([min(abs(ux.GetBounds()[0]), abs(ux.GetBounds()[1])),
                                      min(abs(uy.GetBounds()[0]), abs(uy.GetBounds()[1]))])
                segment.SetVelBounds([min(abs(vx.GetBounds()[0]), abs(vx.GetBounds()[1])),
                                      min(abs(vy.GetBounds()[0]), abs(vy.GetBounds()[1]))])
                controlSegements.append(segment)
                prev_controls[vx] = vxf
                prev_controls[vy] = vyf

        return controlSegements

    def isEqual(self, l1, l2):
        if len(l1) != len(l2):
            return False
        for i in xrange(len(l1)):
            if l1[i] != l2[i]:
                return False
        return True


class Event():
    def __init__(self, index, startTime, duration, action, isStart, states, inputs, relatedEvent):
        self.index = index
        self.startTime = startTime
        self.duration = duration
        self.endtime = startTime + duration
        self.activity = action
        self.isStart = isStart
        self.states = states
        self.inputs = inputs
        self.relatedEvent = relatedEvent
        if self.isStart:
            self.eventName = "START-" + self.activity
        else:
            self.eventName = "  END-" + self.activity

    def __str__(self):
        return self.eventName

    def ToString(self):
        st = str(self.index) + "\t" + "{0:.3f}".format(self.startTime) + "\t[ " + "{0:.3f}".format(self.duration) \
                + " :\t" + str(self.relatedEvent) + "]\t" + self.eventName + "\t" + self.Dic2String(self.states) + "\t" + self.Dic2String(self.inputs)
        return st


    @property
    def Name(self):
        return self.eventName

    @Name.setter
    def Name(self, newName):
        self.eventName = newName

    @property
    def Duration(self):
        return self.duration

    @property
    def Index(self):
        return self.index

    @property
    def StartTime(self):
        return self.startTime

    @property
    def States(self):
        return self.states

    @property
    def Controls(self):
        return self.inputs

    def Dic2String(self, dic):
        st = ""
        for key in dic.keys():
            if type(dic[key]) is float:
                val = "{0:.3f}".format(dic[key])
            else:
                val = str(key)
            st = st + str(key) + ": " + val + ", "
        return st


class Segment():
    def __init__(self, index, activity, startTime, finalTime, init_states, final_states, init_controls, final_controls):
        self.activity = activity
        self.index = index
        self.startTime = startTime
        self.finalTime = finalTime
        self.initStates = init_states
        self.finalStates = final_states
        self.initControls = init_controls
        self.finalControls = final_controls

    @property
    def Activity(self):
        return self.activity

    def __str__(self):
        return self.activity

    def GetInitStates(self):
        return self.initStates.keys()

    def GetInitInputs(self):
        return self.initControls.keys()

    def ToString(self):
        duration = self.finalTime - self.startTime
        st = str(self.index) + "\t" + "{0:.3f}".format(self.startTime) + "\t" + "{0:.3f}".format(self.finalTime) \
                + "\t" + self.activity #+ "\tInit: " + self.Dic2String(self.initStates) + "\tFinal: " + self.Dic2String(self.finalStates)
        return st

    def Dic2String(self, dic):
        st = ""
        for key in dic.keys():
            if type(dic[key]) is float:
                val = "{0:.3f}".format(dic[key])
            else:
                val = str(key)
            st = st + str(key) + ": " + val + ", "
        return st


class LinearControlSegment():
    def __init__(self):
        self._Duration = 0
        self._x0 = 0
        self._xf = 0
        self._U = 1000000
        self._V = 1000000
        return

    @property
    def V(self):
        return self._V

    @V.setter
    def V(self, value):
        self._V = abs(value)

    @property
    def U(self):
        return self.U

    @U.setter
    def U(self, value):
        self._U = abs(value)

    @property
    def Duration(self):
        return self._Duration

    @Duration.setter
    def Duration(self, dur):
        self._Duration = dur

    @property
    def x0(self):
        return self._x0

    @x0.setter
    def x0(self, value):
        self._x0 = value

    @property
    def xf(self):
        return self._xf

    @xf.setter
    def xf(self, value):
        self._xf = value


class ControlSegment():
    def __init__(self, sys, event, ID):
        self._x = LinearControlSegment()
        self._y = LinearControlSegment()
        self.duration = 0
        self._k = 0.05
        self._alpha = 0.1
        self._m = 1
        self.system = sys
        self.event = event
        self.eventID = ID

    def SetDuration(self, T):
        T = round(T, 3)
        self._x.Duration = T
        self._y.Duration = T
        self.duration = T

    def SetInitConditions(self, x0, y0):
        self._x.x0 = x0
        self._y.x0 = y0
        return

    def SetFinalConditions(self, xf, yf):
        self._x.xf = xf
        self._y.xf = yf
        return

    def ToString(self):
        st = self.system, self._x.x0, self._x.xf, self._y.x0, self._y.xf, self.duration
        return st

    def SetAccBounds(self, bounds):
        self._x.U = bounds[0]
        self._y.U = bounds[1]
        pass

    def SetVelBounds(self, bounds):
        self._x.V = bounds[0]
        self._y.V = bounds[1]

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    # @property
    # def U(self):
    #     return self._U
    #
    # @U.setter
    # def U(self, value):
    #     self._U = value
    #
    # @property
    # def V(self):
    #     return self._V
    #
    # @V.setter
    # def V(self, value):
    #     self._V = value

    @property
    def k(self):
        return  self._k

    @k.setter
    def k(self, value):
        self._k = value

    @property
    def m(self):
        return self._m

    @m.setter
    def m(self, value):
        self._m = value

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        self._alpha = value









