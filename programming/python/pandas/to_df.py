import pandas as pd

data_list = [
    {'Name': 'Alice', 'Age': 40, 'Point': 80},
    {'Name': 'Bob', 'Age': 20},
    {'Name': 'Charlie', 'Age': 30, 'Point': 70}
]

df = pd.DataFrame(data_list)
print(df)