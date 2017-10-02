import json
import os

jsonpath = 'E:\\git\\shiyanlou\\week2\\first\\files'
jsonfilenames = os.listdir(jsonpath)


def jsonfile(jsonfilename):
    with open(os.path.join(jsonpath, jsonfilename), 'r') as jsonfile:
        jsonfilecontent = json.loads(jsonfile.read())
        print(jsonfilecontent)
    return jsonfilecontent

if __name__ == '__main__':
    titles = []
    for jsonfilename in jsonfilenames:
        title = jsonfile(jsonfilename)['title']
        titles.append(title)
    print(titles)