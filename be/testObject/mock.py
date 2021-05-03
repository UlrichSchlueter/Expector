#!/usr/bin/env python3

import yaml
import sys
import pprint
import time
import subprocess


class Action:
    def __init__(self, name, command):
        self.name = name
        self.command = command
        self.sp = None


pp = pprint.PrettyPrinter(indent=4)

timetable = sys.argv[1]

DONE = "done"
startTime = time.time()


print(timetable)


def checkActions(actions):
    # print("---Running---")
    noneCounter = 0
    for x in actions:
        res = x.sp.poll()
        if res is None:
            noneCounter += 1
            print(x.name)
    #print (len(actions),"<-->",noneCounter)
    return noneCounter


with open(timetable) as file:
    triggers = yaml.full_load(file)
    # pp.pprint(triggers)

x = 5
all = len(triggers)
actions = []

processTestTime = 3

while x > 0:

    time.sleep(1)
    newTime = time.time()-startTime
    done = 0
    for trigger in triggers:
        #print (trigger['after'])
        shouldBe = trigger['after']
        cmd = trigger['command']
        name = trigger['name']
        if DONE in trigger:
            done += 1
        elif shouldBe < newTime:
            print("Triggering:", name, cmd)
            trigger["done"] = newTime
            sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, universal_newlines=True)
            action = Action(name, cmd)
            action.sp = sp
            actions.append(action)
            done += 1
    if done == all:
        break
    if processTestTime < newTime:
        processTestTime += 3
        checkActions(actions)
n = 1
while n > 0:
    n = checkActions(actions)
    time.sleep(1)

print("Fineeze")
