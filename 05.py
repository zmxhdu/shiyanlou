import sys
import os
import queue
import getopt
import configparser
import datetime
from multiprocessing import Process, Queue

infos = sys.argv
options, args = getopt.getopt(infos[1:], 'C:c:d:o:')


# if len(infos) != 7:
#     print("Parameter Error")
#     exit()

infospath = os.getcwd()
for option in options:
    if option[0] == '-c':
        if '/' in option[1]:
            config_filename = option[1]
        else:
            config_filename = infospath + '/' + option[1]
    elif option[0] == '-d':
        if '/' in option[1]:
            user_filename = option[1]
        else:
            user_filename = infospath + '/' + option[1]
    elif option[0] == '-o':
        if '/' in option[1]:
            result_filename = option[1]
        else:
            result_filename = infospath + '/' + option[1]
    elif option[0] == '-C':
        city_name = str.upper(option[1])
        if city_name:
            city_name = city_name
        else:
            city_name = 'DEFAULT'

q_userdata = Queue()
q_result = Queue()


class Config(object):
    def __init__(self, city_name, config_name):
        self._city_name = city_name
        self._config_name = config_name

    def get_config(self):
        configdir = {}
        if (config_filename is "") or (self._config_name is ""):
            print("Parameter Error")
            return "Parameter Error"
        try:
            cf = configparser.ConfigParser()
            cf.read(config_filename)
            for item in cf.items(self._city_name):
                config_name = item[0].strip()
                config_value = item[1].strip()
                if (config_name is "") or (config_value is ""):
                    print("Parameter Error")
                    exit()
                configdir[config_name] = config_value
            return float(configdir[str.lower(self._config_name)])
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

    JiShuL = Config(city_name, 'JiShuL').get_config()
    JiShuH = Config(city_name, 'JiShuH').get_config()
    YangLao = Config(city_name, 'YangLao').get_config()
    YiLiao = Config(city_name, 'YiLiao').get_config()
    ShiYe = Config(city_name, 'ShiYe').get_config()
    GongShang = Config(city_name, 'GongShang').get_config()
    ShengYu = Config(city_name, 'ShengYu').get_config()
    GongJiJin = Config(city_name, 'GongJiJin').get_config()
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
            time = datetime.datetime.now()
            time = datetime.datetime.strftime(time,"%Y-%m-%d %H:%M:%S")
            data = data + [JiShu * premium,ratal * rate - deduction,real_salary,time]
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
                                  str(format(data[4], '.2f')) + ',' + \
                                  data[5] + '\n'))


if __name__ == '__main__':
    workers = [
        UserData(),
        Calculator(),
        Result()
    ]
    for worker in workers:
        worker.run()
