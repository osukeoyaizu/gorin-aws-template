import json

# ヘッダーとデータ
header = ["ID", "都道府県名", "平成30年面積(k㎡)"]
rows = [
    ["0", "北海道", "83423.83"],
    ["2", "岩手県", "15275.01"],
    ["4", "秋田県", "11637.52"],
    ["6", "福島県", "13783.9"],
    ["14", "新潟県", "12584.23"],
    ["19", "長野県", "13561.56"],
    ["20", "岐阜県", "10621.29"]
]

# JSONに変換（1行ずつ辞書にする）
json_list = []
for row in rows:
    item = {}
    for i in range(len(header)):
        item[header[i]] = row[i]
    json_list.append(item)

# 整形して表示
print(json.dumps(json_list, ensure_ascii=False, indent=2))