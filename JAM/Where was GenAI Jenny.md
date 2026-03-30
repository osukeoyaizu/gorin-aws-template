## task1
Lambdaのコンソール画面からS3のトリガーを作成する

## task2
**Nova Liteのモデルアクセスを有効化する**
## Lambda関数のコードを修正する
**※リージョンによってはモデルIDを「mistral.mistral-large-2402-v1:0」に変更する必要がある**
```
user_msg = '''
instruction = You are an assistant that analyzes big pieces of text and extracts date-location pairs. Read the provided block of text and extract every date (The date contains both day, month and year) and its corresponding location (city) out of it. 
Put these extracted dates and locations into an output sequence that is structured like this: items = [{'Date': 'Month1 Day1, Year1', 'Location': 'City1'},    {'Date': 'Month2 Day2, Year2', 'Location': 'City2'}, etc.]. An example of a shorter text will be provided below. Do the same type of extraction on our longer text 
### Example:
input-example = GenAI Jenny went on January 15, 2025, to Las Vegas and afterwards on February 10, 2025, to Tokyo.
output-example = 
items = [
{'Date': 'January 15, 2025', 'Location': 'Las Vegas'},
{'Date': 'February 10, 2025', 'Location': 'Tokyo'}
] 
### Now, process the following input: = ''' + input_text
```
