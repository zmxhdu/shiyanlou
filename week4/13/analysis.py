import json
import pandas as pd

def analysis(file, user_id):
    times = 0
    minutes = 0
    with open(file,'r') as user_file:
        users = json.loads(user_file.read())
        df = pd.DataFrame(users)
        times = df[df['user_id']==user_id]['user_id'].count()
        minutes = df[df['user_id']==user_id]['minutes'].sum()

        return times, minutes


