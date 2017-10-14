import json
import pandas as pd
import matplotlib.pyplot as plt


def analysis():
    with open('/home/shiyanlou/Code/user_study.json','r') as user_file:
        x = []
        y = []
        users = json.loads(user_file.read())
        userdf = pd.DataFrame(users)
        for i in range(0,len(users)):
            id = users[i]['user_id']
            minutes = userdf[userdf['user_id']==id]['minutes'].sum()
            x.append(id)
            y.append(minutes)
        return x, y


if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_title("StudyData")

    ax.set_xlabel("User ID")
    ax.set_ylabel("Study Time")

    x, y = analysis()
    ax.plot(x, y)
    plt.show()

