import sys
import os
import queue
from multiprocessing import Process, Queue

infos = sys.argv

if len(infos) != 7:
    print("Parameter Error")
    exit()

infospath = os.getcwd()
for i in range(0, len(infos)):
    if infos[i] == '-c':
        if '/' in infos[i + 1]:
            config_filename = infos[i + 1]
        else:
            config_filename = infospath + '/' + infos[i + 1]
    elif infos[i] == '-d':
        if '/' in infos[i + 1]:
            user_filename = infos[i + 1]
        else:
            user_filename = infospath + '/' + infos[i + 1]
    elif infos[i] == '-o':
        if '/' in infos[i + 1]:
            result_filename = infos[i + 1]
        else:
            result_filename = infospath + '/' + infos[i + 1]

q_userdata = Queue()
q_result = Queue()


class Config(object):
    def __init__(self, config_filename, config_name):
        self._config_filename = config_filename
        self._config_name = config_name

    def get_config(self):
        configdir = {}
        if (self._config_filename is "") or (self._config_name is ""):
            print("Parameter Error")
            return "Parameter Error"
        try:
            with open(self._config_filename) as config_file:
                for line in config_file:
                    configs = line.split("=", )
                    if len(configs) != 2:
                        print("Parameter Error")
                        exit()
                    config_name = configs[0].strip()
                    config_value = configs[1].strip()
                    if (config_name is "") or (config_value is ""):
                        print("Parameter Error")
                        exit()
                    configdir[config_name] = config_value
            return float(configdir[self._config_name])
        except FileNotFoundError:
            print("Parameter Error")
            exit()

class UserData(Process):

    def get_user(self):
        if (user_filename is ""):
            print("Parameter Error")
            exit()
        try:
            with open(user_filename) as user_file:
                for lines in user_file:
                    users = lines.split(",", )
                    if len(users) != 2:
                        print("Parameter Error")
                        exit()
                    user_num = users[0].strip()
                    user_salary = users[1].strip()
                    if (user_num is "") or (user_salary is ""):
                        print("Parameter Error")
                        exit()
                    user_salary = int(user_salary)
                    yield (user_num, user_salary)
        except FileNotFoundError:
            print("Parameter Error")
            exit()
    def run(self):
        for data in self.get_user():
            q_userdata.put(data)


class Calculator(Process):
    global premium, JiShuL, JiShuH, threshold

    JiShuL = Config(config_filename, 'JiShuL').get_config()
    JiShuH = Config(config_filename, 'JiShuH').get_config()
    YangLao = Config(config_filename, 'YangLao').get_config()
    YiLiao = Config(config_filename, 'YiLiao').get_config()
    ShiYe = Config(config_filename, 'ShiYe').get_config()
    GongShang = Config(config_filename, 'GongShang').get_config()
    ShengYu = Config(config_filename, 'ShengYu').get_config()
    GongJiJin = Config(config_filename, 'GongJiJin').get_config()
    premium = YangLao + YiLiao + ShiYe + GongShang + ShengYu + GongJiJin
    threshold = 3500


    def calculator(self):
        while True:
            try:
                user_num, user_salary = q_userdata.get(timeout=1)
            except queue.Empty:
                return
            data = [user_num,user_salary]
            if 0 < user_salary < JiShuL:
                JiShu = JiShuL
            elif user_salary > JiShuH:
                JiShu = JiShuH
            else:
                JiShu = user_salary

            if (user_salary - threshold) > 0:
                ratal = user_salary - JiShu * premium - threshold
            else:
                ratal = 0

            if ratal <= 1500:
                rate = 3 / 100
                deduction = 0
            elif ratal <= 4500:
                rate = 10 / 100
                deduction = 105
            elif ratal <= 9000:
                rate = 20 / 100
                deduction = 555
            elif ratal <= 35000:
                rate = 25 / 100
                deduction = 1005
            elif ratal <= 55000:
                rate = 30 / 100
                deduction = 2755
            elif ratal <= 80000:
                rate = 35 / 100
                deduction = 5505
            else:
                rate = 45 / 100
                deduction = 13505
            real_salary = user_salary - JiShu * premium - (ratal * rate - deduction)
            data = data + [JiShu * premium,ratal * rate - deduction,real_salary]
            yield data

    def run(self):
        for data in self.calculator():
            q_result.put(data)


class Result(Process):
    def run(self):
        while True:
            try:
                data = q_result.get(timeout=1)
            except queue.Empty:
                return
            with open(result_filename, 'a') as resultfile:
                resultfile.writelines((str(data[0]) + ',' + \
                                  str(data[1]) + ',' + \
                                  str(format(data[2], '.2f')) + ',' + \
                                  str(format(data[3], '.2f')) + ',' + \
                                  str(format(data[4], '.2f')) + '\n'))


if __name__ == '__main__':
    workers = [
        UserData(),
        Calculator(),
        Result()
    ]
    for worker in workers:
        worker.run()