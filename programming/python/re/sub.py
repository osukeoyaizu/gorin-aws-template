import re

name = 'Crystal White' ## → Crystal *****
email = 'davisjesus@example.org' ## d*********@example.org
phone_number = '010-7658-5153' ## 010-7658-****


## nameの空白以降の値を*に置換
pattern = r"\s+.*$"
repl = lambda m: " " + "*" * (len(m.group(0)) - 1)
masked_name = re.sub(pattern, repl, name)
print(masked_name) 

## emailの@前の一文字目以外を*に置換
pattern = r"(^.)([^@]*)(@.*$)"
repl = lambda m: m.group(1) + "*" * len(m.group(2)) + m.group(3)
masked_email= re.sub(pattern, repl, email)
print(masked_email) 


## phone_numberの最後の-以降を*に置換
pattern = r"(.+-)([^-]+)$"
repl = lambda m: m.group(1) + "*" * len(m.group(2))
masked_email= re.sub(pattern, repl, phone_number)
print(masked_email)
