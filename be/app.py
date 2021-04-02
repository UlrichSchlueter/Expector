from flask import Flask, escape, request, jsonify
from flask import render_template
from flask_cors import CORS
from flask_executor import Executor
import expector
import time

count = 0
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

executor = Executor(app)

# enable CORS


expectors = []


class ExpectorRunner:
    def __init__(self, executor, filename, index):
        self.executor = executor
        self.expector = None
        self.filename = filename
        self.key = filename+" "+str(index)
        self.state = "init"
        self.index = index

    def triggerRun(self):

        fb = executor.submit_stored(self.key, self.runExecutor, "x")
        fb.add_done_callback(self.callback)

    def runExecutor(self, x):
        print("Run:", self.key)
        self.state = "Running"
        try:
            e = expector.Expector(self.filename)
            expectors.append(self)
            self.expector = e
            e.run()

            print("Ran:", self.key)
        except Exception as e:
            print("Failed", e)
            self.state = "Failed"

    def callback(self, future):
        print("Finished"+self.key)
        self.state = "Finished"

        future2 = self.executor.futures.pop(self.key)
        # expectors.remove(self)


def expectorsToJson():
    dict = {}
    for e in expectors:
        dict[e.key] = {"state": e.state, "index": e.index}
    return jsonify(dict)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/startTask/<filename>')
def start_task(filename):
    global count
    count += 1
    er = ExpectorcRunner(executor, filename, count)
    er.triggerRun()

    return jsonify({'result': 'success:'+str(count)})


@app.route('/getResult')
def get_result():

    return expectorsToJson()


@app.route('/getSensors')
def getsensors():
    dict = {}
    for e in expectors:
        if len(e.expector.lastRun.values()) > 0:
            dict[e.key] = e.expector.lastRun
    return jsonify(dict)


@app.route('/getMetrics/<state>')
def getmetrics(state):
    dict = {}
    for e in expectors:
        if (e.state == state):
            dict[e.key] = {'name': e.key, 'state': e.state}
            metrices = []
            for exp in e.expector.expecters:
                eee = e.expector.expecters[exp]
                metrices.append(
                    {'name': eee.metric})
            dict[e.key]['metrices'] = metrices
        # if len(e.expector.lastRun.values()) > 0:
        #    dict[e.key] = {"metric": e.expector.state}
    return jsonify(dict)


@ app.route('/getRuns/<state>')
def getRuns(state):
    dict = {}
    for e in expectors:
        if (e.state == state):
            dict[e.key] = {'name': e.key, 'state': e.state}
            metrices = []
            for exp in e.expector.expecters:
                eee = e.expector.expecters[exp]
                metrices.append(
                    {'name': eee.metric, "whendone": eee.whenDone})
            dict[e.key]['metrices'] = metrices
        # if len(e.expector.lastRun.values()) > 0:
        #    dict[e.key] = {"metric": e.expector.state}
    return jsonify(dict)


@ app.route('/getRunData/<runid>')
def getRunData(runid):
    metrices = []
    for e in expectors:
        if (e.key == runid):
            for exp in e.expector.expecters:
                eee = e.expector.expecters[exp]
                steps = []
                for step in eee.steps:
                    steps.append(step.serialize())
                currentStep = eee.getCurrentStep()
                if currentStep is None:
                    currentStepJson = None
                else:
                    currentStepJson = eee.getCurrentStep().serialize()
                metrices.append(
                    {'name': eee.metric, 'finished': eee.finished, "whendone": eee.whenDone, "steps": steps,
                     "currentStep": currentStepJson}
                )
            break
        # if len(e.expector.lastRun.values()) > 0:
        #    dict[e.key] = {"metric": e.expector.state}
    return jsonify(metrices)
