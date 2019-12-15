import json
import sys


if __name__ == '__main__':
    filenamelist = sys.argv[1:]
    print(sys.argv)
    t = 500
    for filename in filenamelist:
        with open(filename) as f:
            data = json.load(f)
            for i, action in enumerate(data["action set"]):
                if data["action set"][i]["action name"] == 'delay':
                    data["action set"][i]["param"] = t
        try:
            with open(filename, "w") as f:
                json.dump(data, f)
        except:
            print('save file failed')