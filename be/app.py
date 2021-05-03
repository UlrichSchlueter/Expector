from flask import Flask, escape, request, jsonify
from flask import render_template
from flask_cors import CORS
from flask_executor import Executor
import expector
import time
from datetime import datetime

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
        self.startTime = None
        self.endTime = None

    def triggerRun(self):

        fb = executor.submit_stored(self.key, self.runExecutor, "x")
        fb.add_done_callback(self.callback)
        self.startTime = datetime.now()

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
        self.endTime = datetime.now()
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
    er = ExpectorRunner(executor, filename, count)
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
            dict[e.key] = {'name': e.key, 'state': e.state, 'id': e.index,
                           'filename': e.filename, "startTime": e.startTime, "endTime": e.endTime}
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
            dict[e.key] = {'name': e.key, 'state': e.state, 'id': e.index,
                           'filename': e.filename, "startTime": e.startTime, "endTime": e.endTime}
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
                    {'name': eee.metric, 'finished': eee.isFinished, "whendone": eee.whenDone, "steps": steps,
                     "currentStep": currentStepJson}
                )
            break
        # if len(e.expector.lastRun.values()) > 0:
        #    dict[e.key] = {"metric": e.expector.state}
    return jsonify(metrices)


@ app.route('/getGraph/<runid>')
def getGraph(runid):
    dependencies = {}
    for e in expectors:
        if (e.key == runid):
            dependencies = e.expector.getDependencyState()
            break
    return jsonify(dependencies)


@app.route('/getNetworkData/<runid>')
def getNetworkData(runid):
    graph: {'nodes':
            [
                {'name': 'Lillian', 'sex': 'F'},
                {'name': 'Gordon', 'sex': 'M'},
                {'name': 'Sylvester', 'sex': 'M'},
                {'name': 'Mary', 'sex': 'F'},
                {'name': 'Helen', 'sex': 'F'},
                {'name': 'Jamie', 'sex': 'M'},
                {'name': 'Jessie', 'sex': 'F'},
                {'name': 'Ashton', 'sex': 'M'},
                {'name': 'Duncan', 'sex': 'M'},
                {'name': 'Evette', 'sex': 'F'},
                {'name': 'Mauer', 'sex': 'M'},
                {'name': 'Fray', 'sex': 'F'},
                {'name': 'Duke', 'sex': 'M'},
                {'name': 'Baron', 'sex': 'M'},
                {'name': 'Infante', 'sex': 'M'},
                {'name': 'Percy', 'sex': 'M'},
                {'name': 'Cynthia', 'sex': 'F'},
                {'name': 'Feyton', 'sex': 'M'},
                {'name': 'Lesley', 'sex': 'F'},
                {'name': 'Yvette', 'sex': 'F'},
                {'name': 'Maria', 'sex': 'F'},
                {'name': 'Lexy', 'sex': 'F'},
                {'name': 'Peter', 'sex': 'M'},
                {'name': 'Ashley', 'sex': 'F'},
                {'name': 'Finkler', 'sex': 'M'},
                {'name': 'Damo', 'sex': 'M'},
                {'name': 'Imogen', 'sex': 'F'}
            ],
            'links':
            [
                {'source': 'Sylvester', 'target': 'Gordon', 'type': 'A'},
                {'source': 'Sylvester', 'target': 'Lillian', 'type': 'A'},
                {'source': 'Sylvester', 'target': 'Mary', 'type': 'A'},
                {'source': 'Sylvester', 'target': 'Jamie', 'type': 'A'},
                {'source': 'Sylvester', 'target': 'Jessie', 'type': 'A'},
                {'source': 'Sylvester', 'target': 'Helen', 'type': 'A'},
                {'source': 'Helen', 'target': 'Gordon', 'type': 'A'},
                {'source': 'Mary', 'target': 'Lillian', 'type': 'A'},
                {'source': 'Ashton', 'target': 'Mary', 'type': 'A'},
                {'source': 'Duncan', 'target': 'Jamie', 'type': 'A'},
                {'source': 'Gordon', 'target': 'Jessie', 'type': 'A'},
                {'source': 'Sylvester', 'target': 'Fray', 'type': 'E'},
                {'source': 'Fray', 'target': 'Mauer', 'type': 'A'},
                {'source': 'Fray', 'target': 'Cynthia', 'type': 'A'},
                {'source': 'Fray', 'target': 'Percy', 'type': 'A'},
                {'source': 'Percy', 'target': 'Cynthia', 'type': 'A'},
                {'source': 'Infante', 'target': 'Duke', 'type': 'A'},
                {'source': 'Duke', 'target': 'Gordon', 'type': 'A'},
                {'source': 'Duke', 'target': 'Sylvester', 'type': 'A'},
                {'source': 'Baron', 'target': 'Duke', 'type': 'A'},
                {'source': 'Baron', 'target': 'Sylvester', 'type': 'E'},
                {'source': 'Evette', 'target': 'Sylvester', 'type': 'E'},
                {'source': 'Cynthia', 'target': 'Sylvester', 'type': 'E'},
                {'source': 'Cynthia', 'target': 'Jamie', 'type': 'E'},
                {'source': 'Mauer', 'target': 'Jessie', 'type': 'E'},
                {'source': 'Duke', 'target': 'Lexy', 'type': 'A'},
                {'source': 'Feyton', 'target': 'Lexy', 'type': 'A'},
                {'source': 'Maria', 'target': 'Feyton', 'type': 'A'},
                {'source': 'Baron', 'target': 'Yvette', 'type': 'E'},
                {'source': 'Evette', 'target': 'Maria', 'type': 'E'},
                {'source': 'Cynthia', 'target': 'Yvette', 'type': 'E'},
                {'source': 'Maria', 'target': 'Jamie', 'type': 'E'},
                {'source': 'Maria', 'target': 'Lesley', 'type': 'E'},
                {'source': 'Ashley', 'target': 'Damo', 'type': 'A'},
                {'source': 'Damo', 'target': 'Lexy', 'type': 'A'},
                {'source': 'Maria', 'target': 'Feyton', 'type': 'A'},
                {'source': 'Finkler', 'target': 'Ashley', 'type': 'E'},
                {'source': 'Sylvester', 'target': 'Maria', 'type': 'E'},
                {'source': 'Peter', 'target': 'Finkler', 'type': 'E'},
                {'source': 'Ashley', 'target': 'Gordon', 'type': 'E'},
                {'source': 'Maria', 'target': 'Imogen', 'type': 'E'}
            ]
            }

    return jsonify(elements)
