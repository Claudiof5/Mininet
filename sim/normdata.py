import pandas as pd
import sys

args = list(sys.argv)
args.pop(0)

def normalize_time(norm):
    if norm == "1/24":
        return 3600/86400
    elif norm == "1/1":
        return 1
    elif norm == "1/720":
        return 3600/2592000
    
def convert_to_seconds(x):
    time = x.hour * 3600 + x.minute * 60 + x.second
    return time
    
norm_const = normalize_time(args[1])

dataset = pd.read_csv(args[0])
dataset['timeStamp'] = pd.to_datetime(dataset['timeStamp'])
dataset['seconds'] = dataset['timeStamp'].apply(convert_to_seconds)
dataset['normalized'] = dataset['seconds'] * norm_const
##
lista = []
for i in range(0,len(dataset)):
    if i+1 <= len(dataset)-1:
        data = dataset.loc[i+1,'normalized'] - dataset.loc[i,'normalized']
        if data < 0:
            data = data * (-1)
        lista.append(data)
# O ultimo não espera nada, então:
lista.append(0)

dataset['sleep'] = lista

dataset.to_csv('norm_dataset.csv', index = True)


