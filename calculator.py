import sys
import os

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
        print(config_filename)
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


class UserData(object):
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

    def __init__(self, user_filename):
        self._user_filename = user_filename

    def get_user(self):
        userdir = {}
        if (self._user_filename is ""):
            print("Parameter Error")
            exit()
        try:
            with open(self._user_filename) as user_file:
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
                    userdir[user_num] = user_salary
                    user_salary = int(user_salary)

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
                    with open(result_filename, 'a') as resultfile:
                        resultfile.writelines(str(user_num) + ',' + \
                                              str(user_salary) + ',' + \
                                              str(format(JiShu * premium, '.2f')) + ',' + \
                                              str(format(ratal * rate - deduction, '.2f')) + ',' + \
                                              str(format(real_salary, '.2f')) + '\n')
        except FileNotFoundError:
            print("Parameter Error")
            exit()


usersalary = UserData(user_filename).get_user()
