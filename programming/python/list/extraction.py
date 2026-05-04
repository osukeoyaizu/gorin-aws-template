arr = [0,1,2,3,4,5,6,7,8,9]

# 先頭から「3個」取り出す（インデックス 0 ～ 2）
print(arr[:3])
# → [0, 1, 2]

# 末尾から「3個」を除いた部分を取り出す
print(arr[:-3])
# → [0, 1, 2, 3, 4, 5, 6]

# インデックス 5 から最後までを取り出す
print(arr[5:])
# → [5, 6, 7, 8, 9]

# インデックス 3 から 5 の手前（=4）までを取り出す
print(arr[3:5])
# → [3, 4]

# 先頭から最後まで、2つ飛ばしで取り出す
print(arr[::2])
# → [0, 2, 4, 6, 8]

# 配列を逆順にする
print(arr[::-1])
# → [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]


arr_sorted = sorted(arr)
print(arr_sorted)
arr_sorted_desc = sorted(arr, reverse=True)
print(arr_sorted_desc)
