from flask import Flask, escape, request,jsonify
from flask import render_template
from flask_executor import Executor
import expector
import time

count=0
app = Flask(__name__)
executor = Executor(app)

expectors=[]

class ExpectorcRunner:     
    def __init__(self, executor, filename,index):
        self.executor=executor      
        self.expector=None
        self.filename=filename
        self.key=filename+" "+str(index)
        self.state="init"
        self.index=index

    def triggerRun(self):       
        
        fb=executor.submit_stored(self.key, self.runExecutor,"x")        
        fb.add_done_callback(self.callback)
        
        

    def runExecutor(self,x):      
        print("Run:",self.key)
        self.state="Running"
        try:                          
            e=expector.Expector(self.filename)
            expectors.append(self)    
            self.expector=e
            e.run()
            
            print("Ran:",self.key)
        except Exception as e:
            print ("Failed", e)
            self.state="Failed"            

    def callback(self,future):
        print ("Finished"+self.key)
        self.state="Finished"  
        
        future2=self.executor.futures.pop(self.key)
        #expectors.remove(self)
       


def expectorsToJson():
    dict ={}
    for e in expectors:
        dict[e.key]={"state": e.state, "index": e.index}
    return jsonify(dict)

@app.route('/')
def hello():
    return render_template('index.html')

   
 

@app.route('/startTask/<filename>')
def start_task(filename):    
    global count
    count+=1 
    er=ExpectorcRunner(executor,filename,count)
    er.triggerRun()   
   
    return jsonify({'result':'success:'+str(count)})

@app.route('/getresult')
def get_result():
               
    return expectorsToJson()


@app.route('/getsensors')
def getsensors():
    dict ={}
    for e in expectors:
        if len(e.expector.lastRun.values())>0:
            dict[e.key]={"sensors": e.expector.lastRun}
    return jsonify(dict)           

@app.route('/getmetrics')
def getmetrics():
    dict ={}
    for e in expectors:
        if len(e.expector.lastRun.values())>0:
            dict[e.key]={"metric": e.expector.state}
    return jsonify(dict)           


