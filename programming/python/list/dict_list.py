# 辞書のリストを特定のキーの値でソート
data_list = [{'Name': 'Alice', 'Age': 40, 'Point': 80},
     {'Name': 'Bob', 'Age': 20},
     {'Name': 'Charlie', 'Age': 30, 'Point': 70}]


sort_list = sorted(data_list, key=lambda x: x['Age']) # 昇順
# sort_list = sorted(data_list, key=lambda x: x['Age'], reverse=True) # 降順



# 辞書のリストを特定のキーの最大値を取得
max_age = max(item['Age'] for item in data_list)
print(max_age)


