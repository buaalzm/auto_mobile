import json


class ActionManage():
    tempAction = {}
    def recordActionSetStart(self, actionSetName):
        self.tempAction = {'action set name': actionSetName, 'action set': []}

    def addClickAction(self, position):
        if len(position)<2:
            print('parameter error')
            return
        action = {'action name':'click'}
        action['param'] = position
        action['cmd'] = 'adb shell input tap {x} {y}'.format(x=position[0], y=position[1])
        self.tempAction['action set'].append(action)

    def addDelayAction(self, delayTime):
        action = {'action name': 'delay'}
        action['param'] = delayTime
        self.tempAction['action set'].append(action)

    def addDragAction(self, paramlist):
        if len(paramlist)<5:
            print('parameter error')
            return
        action = {'action name': 'swipe'}
        action['param'] = paramlist
        action['cmd'] = 'adb shell input swipe {} {} {} {} {}'.format(*paramlist)
        self.tempAction['action set'].append(action)

    def addPressHomeAction(self):
        action = {'action name': 'home'}
        action['cmd'] ='adb shell input keyevent 3'
        self.tempAction['action set'].append(action)

    def addPressReturnAction(self):
        action = {'action name': 'return'}
        action['cmd'] = 'adb shell input keyevent 4'
        self.tempAction['action set'].append(action)

    def recordActionSetFinish(self):
        try:
            with open("../mobile_action/{name}.json".format(name=self.tempAction['action set name']), "w") as f:
                json.dump(self.tempAction, f)
        except:
            print('save file failed')

    def loadActionSet(self, filename):
        with open(filename) as f:
            data = json.load(f)
            return data['action set']


if __name__ == '__main__':
    am = ActionManage()
    am.recordActionSetStart('test')
    am.addDelayAction(500)
    am.addClickAction([100,200])
    am.addDragAction([100,100,200,200,500])
    am.recordActionSetFinish()
    actionList = am.loadActionSet('../mobile_action/test.json')
    print(actionList)
    print(actionList[0]['param'])
