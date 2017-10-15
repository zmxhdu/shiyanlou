# coding = utf-8
import pandas as pd


def quarter_volume():
    data = pd.read_csv('apple.csv', header=0)
    data_df = pd.DataFrame(data).set_index(pd.to_datetime(data['Date']))
    del data_df['Date']
    data_volume_quarter = data_df['Volume'].resample('Q').sum().sort_values()
    second_volume = data_volume_quarter[-2]
    second_volume_date = data_volume_quarter.index[-2]

    return second_volume


if __name__ == '__main__':
    quarter_volume()
