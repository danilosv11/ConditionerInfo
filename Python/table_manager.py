from datetime import datetime
import pandas as pd

table_dir = "con_data.csv"


def upload_data(raw_data):
    raw_data = raw_data.split("\n")
    fixed_data = datetime.now().strftime("%d/%m/%Y %H:%M:%S").split()
    for i in range(len(raw_data)):
        fixed_data.append(raw_data[i].split()[1].strip())
    new_data = {'Date': [f'{fixed_data[0]}'], 'Time': [f'{fixed_data[1]}'],
                'Temperature_IN': [f'{fixed_data[2]}'], 'Humidity_IN': [f'{fixed_data[3]}'],
                'Temperature_OUT': [f'{fixed_data[4]}'], 'Humidity_OUT': [f'{fixed_data[5]}'],
                'Wind_speed': [f'{fixed_data[6]}']}
    df = pd.DataFrame(new_data)
    df.to_csv('con_data.csv', mode='a', index=False, header=None, sep=";")
    return


def get_last_data():
    f = open(table_dir, "r")
    data = f.readlines()[-1]
    f.close()
    if data != "":
        return data
    return -1
def get_avg_data():
    df = pd.read_csv(table_dir, sep=';', encoding='latin1', parse_dates=['Date'], dayfirst=True)
    del df["Time"]
    cols = df.columns.difference(['Date'])
    df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
    return df
def get_day_average_data():
    return get_avg_data().set_index('Date').groupby(pd.Grouper(freq='d')).\
        mean().dropna(how='all').tail(7).to_string()
def get_month_average_data():
    return get_avg_data().set_index('Date').groupby(pd.Grouper(freq='ME'))\
        .mean().dropna(how='all').tail(12).to_string()
def get_year_average_data():
    return get_avg_data().set_index('Date').groupby(pd.Grouper(freq='YE'))\
        .mean().dropna(how='all').tail(12).to_string()
