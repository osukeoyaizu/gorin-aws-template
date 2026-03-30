import datetime

# datetime型(mysql timestamp 登録不可)
dt = datetime.datetime.now()
print(dt)
# 2025-03-18 11:31:48.392707
print(type(dt))
# <class 'datetime.datetime'>


# 文字列(mysql timestamp 登録可)
str_dt = datetime.datetime.now().isoformat()
print(str_dt)
# 2025-03-18 11:31:48.392707
print(type(str_dt))
# <class 'str'>


# unixtime
num_dt = datetime.datetime.now().timestamp()
print(num_dt)
# 1742265655.840854
print(type(num_dt))
# <class 'float'>


# datetime→文字列
dt = datetime.datetime.now()
str_dt = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
print(str_dt)
# 2025-03-18 11:31:48.392707
print(type(str_dt))
# <class 'str'>


# unixtime→datetime
tdt = datetime.datetime.fromtimestamp(num_dt)
print(tdt)
# 2025-03-18 13:07:42.703530
print(type(tdt))
# <class 'datetime.datetime'>


# 文字列(isoformat)→datetime
tdt = datetime.datetime.fromisoformat(str_dt)
print(tdt)
# 2025-03-18 13:15:14.936964
print(type(tdt))
# <class 'datetime.datetime'>


# 文字列→datetime
str_dt = 'October 5, 2023'
dt = datetime.datetime.strptime(tdt, "%B %d, %Y")
print(dt)
# 2023-10-05 00:00:00
print(type(dt))
# <class 'datetime.datetime'>

str_dt = '2025-05-22T13:35:44.971584'
dt = datetime.datetime.strptime(str_dt, '%Y-%m-%dT%H:%M:%S.%f')
print(dt)
# 2025-05-22 13:35:44.971584
print(type(dt))
# <class 'datetime.datetime'>


# timedelta
utc_time = '2025-05-22 04:35:49.631493'
print(type(utc_time))
# <class 'datetime.datetime'>
jst_time = utc_time + datetime.timedelta(hours=9)
print(jst_time)
# 2025-05-22 13:35:49.631493
print(type(jst_time))
# <class 'datetime.datetime'>








