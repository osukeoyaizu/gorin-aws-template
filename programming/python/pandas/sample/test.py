import pandas as pd

area = pd.read_csv('area.csv',index_col=0)
pop = pd.read_csv('pop.csv',index_col=0)
cols = area.columns

# # 降順でソート
# print(area.sort_values('平成30年面積(k㎡)',ascending=False))


# # 先頭,末尾から数行だけ取得
# print(area.head(5))
# print(area.tail(5))


# # 条件に合うデータだけを取得する(locを使用すれば取得する列も絞り込める)
# print(area.loc[area['平成30年面積(k㎡)'] >= 10000, ['都道府県名', '平成30年面積(k㎡)']])
# print(area.loc[(area['都道府県名'].isin(['北海道', '鳥取県'])), ['都道府県名', '平成30年面積(k㎡)']])


# # 特定の文字列を含んだデータを抽出
# print(area.loc[area['都道府県名'].str.contains('山')])


# # 特定の文字列を含んだデータ以外を抽出
# print(area.loc[~area['都道府県名'].str.contains('山')])


# # 複数条件
# print(area.loc[
#     (area['都道府県名'].str.contains('県')) & 
#     (area['平成30年面積(k㎡)'] >= 12000)
#     ]
# )


# # カラム名変更
# pop = pop.rename(columns=({'都道府県': '都道府県名'}))  

# # ジョイン
# newarea = pd.merge(pop,area)
# print(type(newarea['総数']))
# print(type(newarea['平成30年面積(k㎡)']))

# # 数値に変換(変換できないものはNaN)
# newarea['総数'] = pd.to_numeric(newarea['総数'], errors='coerce')
# newarea['平成30年面積(k㎡)'] = pd.to_numeric(newarea['平成30年面積(k㎡)'], errors='coerce')

# # 計算した値で新しい列を作成
# newarea['人口密度'] = newarea['総数'] / newarea['平成30年面積(k㎡)']

# # NaNではないデータを抽出する方法
# print(pop.loc[pop['総数'].notna()])

# # NaNデータを置換
# pop.loc[pop['総数'].isnull(), '総数'] = 0





print(area)

