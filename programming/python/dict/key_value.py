# valueの合計値を計算する
d = {"ネットワーク": 60, "データベース": 80, "セキュリティ": 55}
total = sum(d.values())
print(total) #195

# value(string型)の合計値を計算する
d = {"ネットワーク": '60', "データベース": '80', "セキュリティ": '55'}
string_list = d.values()
int_list = [int(s) for s in string_list]
total = sum(int_list)
print(total) #195

d = {'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}

# itemのリスト作成
print(d.items())
# dict_items([('key1', 'val1'), ('key2', 'val2'), ('key3', 'val3')])
print(list(d.items()))
# [('key1', 'val1'), ('key2', 'val2'), ('key3', 'val3')]

# keyのリスト作成
print(d.keys())
# dict_keys(['key1', 'key2', 'key3'])
print(list(d.keys()))
# ['key1', 'key2', 'key3']

# valueのリスト作成
print(d.values())
# dict_values(['val1', 'val2', 'val3'])
print(list(d.values()))
# ['val1', 'val2', 'val3']