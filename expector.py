import yaml
import sys
import pprint
import time
import subprocess
import socket
import os

pp = pprint.PrettyPrinter(indent=4)

expectorfile=sys.argv[1]

DONE="done"
RES="result"
startTime=time.time()

print (expectorfile)



class Expector:
    def __init__(self):
        self.expecters={}
        self.sensors={}
        self.metricResults={}

    def confToExpects(self,expects):
        for e in expects:
            ne=Expect(e["metric"])
            count=0
            for s in e['steps']:
                k=list(s.keys())
                firstItem=k[0]
                ns=Step(firstItem,s[firstItem])
                ne.steps.append(ns)
                count+=1
                ns.id=ne.metric+":"+str(count)
            ne.whenDone=e["whenDone"]
            
            self.expecters[ne.metric]=ne

    def confToSensors(self,sensorList):
        for s in sensorList:
            se=Sensor(s["sensor"])
            if 'comment' in s:
                se.comment=s['comment']
            se.data=s  
            self.sensors[se.name]=se

    def doSensors(self):
        lastRun={}
        for sensor in self.sensors.values():                    
            res=sensor.getSensorData()
            lastRun["sensor."+sensor.name]=res
        return lastRun
    

    def matchExpectors(self, lastRunResults):
        stuffLeftToDo=0
        checkThis={ **self.metricResults, ** lastRunResults}
        pp.pprint(checkThis)
        for e in self.expecters.values():
            if e.finished==False:
                step=e.getCurrentStep()
                if not step is None:
                    sens=step.sensorName.split(".")
                    if sens[0]=="sensor":                        
                        sensor=self.sensors[sens[1]]
                        comment=" ("+ sensor.comment+")"
                    else:
                        comment=""
                    print ("Waiting for " + step.sensorName + comment)
                    stuffLeftToDo+=1
                    if step.sensorName in checkThis:
                        if step.expectedValue==checkThis[step.sensorName]:
                            step.res=step.expectedValue
                            print ("Progressing:"+ step.id)
                else:                    
                    for x in e.whenDone:
                        self.metricResults['metric.'+x]=e.whenDone[x]
                    print ("Metric "+e.metric+ " done.")
                    e.finished=True

        return stuffLeftToDo


class Expect:
    def __init__(self,metric):
        self.metric=metric
        self.steps=[]
        self.whenDone={}
        self.finished=False

    
    def getCurrentStep(self):
        for s in self.steps:
            if s.res is None:
                return s

class Step:
    def __init__(self,sensorName,expectedValue):
        self.sensorName=sensorName
        self.expectedValue=expectedValue
        self.res=None
        self.id=""

class Sensor:
    def __init__(self,name):
        self.name=name
        self.data={}
        self.lastResult=None
        self.file_lastread=0
        self.comment=""

    def getSensorData(self):
        if self.data["type"]=="tcp":
            port=self.data["port"]
            host=self.data["host"]
            res=self.sensor_tcp(host,port)
            self.lastResult=res
        elif self.data["type"]=="filecontent":
            filename=self.data["name"]
            test=self.data["test"]
            res=self.sensor_filecontent(filename,test)
            self.lastResult=res
        else:
            print ("Unknown type"+self.data["type"])
            self.lastResult=None
        return self.lastResult

    def sensor_tcp(self,host,port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((host, port))           
            res=1
        except Exception as e:
            print (e)
            e=e
            res=0
        return res

        

    def sensor_filecontent(self,name,string):
        res=0
        try:
            file_size = os.stat(name)
            if file_size.st_size < self.file_lastread:
                self.file_lastread=0
            with open(name, "r") as f:
                f.seek(self.file_lastread)
                print ("File :"+name + " "+ str(self.file_lastread))
                line = f.readline()
                while line:
                    print ("line:>"+line+"<")
                    if string in line:
                        res=1
                        print ("File string found :"+string)
                        break
                    line = f.readline()                   
                self.file_lastread=f.tell()
            
        except Exception as e:
            print (e)
            e=e
            self.file_lastread=0
        return res



with open(expectorfile) as file:
    config = yaml.full_load(file)
    pp.pprint(config)


app=Expector()
app.confToSensors(config["sensors"])
app.confToExpects(config["expect"])




while True:
    
    lastRunResults=app.doSensors()
    stuffLeftToDo=app.matchExpectors(lastRunResults)
    if stuffLeftToDo==0:
        break   
    
    time.sleep(1)
  

print ("Fineeze")