from PyQt5.QtCore import QThread
import json
import time
import os


class MobileActionExecThread(QThread):
    def setFileNames(self, name_list):
        self.name_list = name_list

    def run(self):
        for name in self.name_list:
            try:
                with open('../mobile_action/' + name + '.json') as f:
                    action_data = json.load(f)
                    print('action set name:{}'.format(action_data['action set name']))
                    for action in action_data['action set']:
                        if action['action name'] == 'delay':
                            print('delay:{}'.format(action['param']))
                            time.sleep(float(action['param']) / 1000)
                        else:
                            print(action['cmd'])
                            os.system(action['cmd'])
            except:
                print('打开文件{}失败'.format(name))
