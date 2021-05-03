import yaml
import sys
import pprint
import time
import subprocess
import socket
import os
import threading
import re

pp = pprint.PrettyPrinter(indent=4)

DONE = "done"
RES = "result"


class Expector:
    def __init__(self, filename):
        self.expecters = {}
        self.sensors = {}
        self.metricResults = {}
        self.file = filename
        self.lastRun = {}
        self.state = {}
        self.allWhenDones = {}
        self.dependencies = {}

        self.loadData()
        self.calcDependencies()

    def loadData(self):
        with open(self.file) as file:
            config = yaml.full_load(file)
            pp.pprint(config)

        self.confToSensors(config["sensors"])
        self.confToExpects(config["expect"])

    def run(self):
        self.startTime = time.time()
        while True:
            self.lastRun = self.doSensors()
            stuffLeftToDo = self.matchExpectors(self.lastRun)
            if stuffLeftToDo == 0:
                break
            time.sleep(3)

    def confToExpects(self, expects):
        for e in expects:
            ne = Expect(e["metric"])

            count = 0
            for s in e['steps']:
                k = list(s.keys())
                firstItem = k[0]
                ns = Step(firstItem, s[firstItem])
                ne.steps.append(ns)
                count += 1
                ns.id = ne.metric + ":" + str(count)
                ns.counter = count
            ne.whenDone = e["whenDone"]
            for key in e["whenDone"]:
                ne.whenDoneValue = e["whenDone"][key]
                self.allWhenDones[key+":"+str(ne.whenDoneValue)] = ne.metric

            self.expecters[ne.metric] = ne

    def confToSensors(self, sensorList):
        for s in sensorList:
            se = Sensor(s["sensor"])
            if 'comment' in s:
                se.comment = s['comment']
            se.data = s
            self.sensors[se.name] = se

    def calcDependencies(self):

        links = []
        nodemap = {}
        nodes = [{'id': 'Start'}]
        nodemap['Start'] = 0
        count = 1
        for e in self.expecters:
            expector = self.expecters[e]
            nodes.append({'id': expector.metric})
            nodemap[expector.metric] = count
            count += 1

        #  {source: 0, target: 1, weight: 10},
        for e in self.expecters:
            expector = self.expecters[e]
            hasDependencies = False
            for s in expector.steps:
                print(e, s)
                if s.sensorName.startswith('metric.'):
                    hasDependencies = True
                    dependsonKey = s.sensorName[7:]
                    dependsonValue = s.expectedValue
                    searchKey = dependsonKey + ":" + str(dependsonValue)
                    if searchKey in self.allWhenDones:
                        m = self.allWhenDones[searchKey]
                        source = nodemap[m]
                        target = nodemap[expector.metric]
                        links.append(
                            {'source': source, 'target': target, 'weight': 10},)
                    else:
                        print("haee ?")
            if hasDependencies == False:
                links.append(
                    {'source': 0, 'target': nodemap[expector.metric], 'weight': 10},)

        self.dependencies['nodes'] = nodes
        self.dependencies['links'] = links

    def getDependencyState(self):
        lastChange = 0
        for e in self.dependencies['nodes']:

            key = e['id']
            if key == 'Start':
                e['isFinished'] = True
                e['stepsLeft'] = 0
                e['stepsDone'] = 0
            else:
                m = self.expecters[key]
                if m.lastChange > lastChange:
                    lastChange = m.lastChange
                e['stepsLeft'] = m.stepsLeft
                e['stepsDone'] = m.stepsDone
                if m.isFinished == True:
                    e['isFinished'] = True
                else:
                    e['isFinished'] = False
        self.dependencies['lastChange'] = lastChange
        return self.dependencies

    def selectSensors(self):
        sensorNames = {}
        for e in self.expecters.values():
            if e.isFinished == False:
                step = e.getCurrentStep()
                if not step is None:
                    sName = step.sensorName
                    if sName in sensorNames:
                        sensorNames[sName] += 1
                    else:
                        sensorNames[sName] = 1
        return sensorNames

    def doSensors(self):
        lastRun = {}
        actions = []
        sensorNames = self.selectSensors()
        for sensor in self.sensors.values():
            sName = "sensor."+sensor.name
            if sName in sensorNames:
                action = SenorAction(sensor.name, sensor)
                action.start()
                actions.append(action)
            else:
                # print("Skipping " + sensor.name)
                pass

        for action in actions:
            action.join()

            lastRun["sensor."+action.sensor.name] = action.sensor.lastResult

        return lastRun

    def matchExpectors(self, lastRunResults):
        stuffLeftToDo = 0
        checkThis = {**self.metricResults, ** lastRunResults}
        pp.pprint(checkThis)
        newState = {}
        for e in self.expecters.values():
            if e.isFinished == False:
                step = e.getCurrentStep()

                if not step is None:
                    sens = step.sensorName.split(".")
                    if sens[0] == "sensor":
                        sensor = self.sensors[sens[1]]
                        comment = " (" + sensor.comment+")"
                    else:
                        comment = ""
                    print("Waiting for " + e.metric+":"+step.sensorName +
                          " to become " + str(step.expectedValue) + comment)
                    newState[e.metric] = {
                        "Step": step.sensorName + ":" + str(step.expectedValue), "Comment": comment}
                    stuffLeftToDo += 1
                    if step.sensorName in checkThis:
                        print(str(step.expectedValue) + "<  vs >" +
                              str(checkThis[step.sensorName]))
                        if str(step.expectedValue) == str(checkThis[step.sensorName]):
                            step.res = step.expectedValue
                            print("Progressing:" + step.id)
                            if e.getCurrentStep() is None:
                                e.setFinished()
                                for x in e.whenDone:
                                    self.metricResults['metric.' +
                                                       x] = e.whenDone[x]
                                    print("Metric "+e.metric + " done.")

                else:
                    for x in e.whenDone:
                        self.metricResults['metric.'+x] = e.whenDone[x]
                    print("Metric " + e.metric + " done.")
                    e.setFinished()
        self.state = newState
        return stuffLeftToDo


class Expect:
    def __init__(self, metric):
        self.metric = metric
        self.steps = []
        self.whenDone = {}
        self.isActive = False
        self.isFinished = False
        self.stepsDone = 0
        self.stepsLeft = 0
        self.lastChange = time.time()
        self.lastStepid = -1

    def getCurrentStep(self):
        count = 0
        for s in self.steps:
            if s.res == '':
                if s.id != self.lastStepid:
                    self.lastStepid = s.id
                    self.lastChange = time.time()
                    self.stepsDone = count
                    self.stepsLeft = len(self.steps)-self.stepsDone
                return s
            count += 1

    def setFinished(self):
        self.isFinished = True
        self.lastChange = time.time()
        self.stepsDone = len(self.steps)
        self.stepsLeft = len(self.steps)-self.stepsDone


class Step:
    def __init__(self, sensorName, expectedValue):
        self.sensorName = sensorName
        self.expectedValue = expectedValue
        self.res = ""
        self.id = ""
        self.counter = 0

    def serialize(self):
        return {"sensorName": self.sensorName,
                "expectedValue": self.expectedValue,
                "result": self.res,
                "id": self.id,
                "counter": str(self.counter)
                }


class SenorAction (threading.Thread):
    def __init__(self, threadID, sensor):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.sensor = sensor

    def run(self):
        self.sensor.getSensorData()


class Sensor:
    def __init__(self, name):
        self.name = name
        self.data = {}
        self.lastResult = None
        self.file_lastread = 0
        self.comment = ""
        self.pattern = re.compile("EXPECT::(.*?)::")

    def getSensorData(self):
        if self.data["type"] == "tcp":
            port = self.data["port"]
            host = self.data["host"]
            res = self.sensor_tcp(host, port)
            self.lastResult = res
        elif self.data["type"] == "filecontent":
            filename = self.data["name"]
            test = self.data["test"]
            res = self.sensor_filecontent(filename, test)
            self.lastResult = res
        elif self.data["type"] == "script":
            cmd = self.data["command"]
            sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = sp.communicate()
            sp.wait(timeout=10)
            fullOutput = stdout+stderr
            found = self.pattern.findall(fullOutput)
            if len(found) == 0:
                self.lastResult = "NO_RESULT_DETECTED"
            else:
                self.lastResult = found[0].strip()
            print(fullOutput)

        else:
            print("Unknown type"+self.data["type"])
            self.lastResult = None
        return self.lastResult

    def sensor_tcp(self, host, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((host, port))
            res = "1"
        except Exception as e:
            print(e)
            e = e
            res = "0"
        return res

    def sensor_filecontent(self, name, string):
        res = "0"
        try:
            file_size = os.stat(name)
            if file_size.st_size < self.file_lastread:
                self.file_lastread = 0
            with open(name, "r") as f:
                f.seek(self.file_lastread)
                # print ("File :"+name + " "+ str(self.file_lastread))
                line = f.readline()
                while line:
                    # print ("line:>"+line+"<")
                    if string in line:
                        res = "1"
                        print("File string found :"+string)
                        break
                    line = f.readline()
                self.file_lastread = f.tell()

        except Exception as e:
            # print (e)
            e = e
            self.file_lastread = 0
        return res


if __name__ == "__main__":
    expectorfile = sys.argv[1]
    e = Expector(expectorfile)
    print(e.dependencies)
    e.run()

    print("Fineeze")
