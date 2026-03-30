import csv
import json

# テキストファイルの読み込み
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

# テキストファイルへの書き込み
def write_text_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# CSVファイルの読み込み
def read_csv_file(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # ヘッダーを取得
        for row in reader:
            data.append(row)
    return header, data


# CSVファイルへの書き込み
def write_csv_file(file_path, header, data):
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)  # ヘッダーを書き込み
        writer.writerows(data)   # データを書き込み


# JSONファイルの読み込み
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


# JSONファイルへの書き込み
def write_json_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# 画像ファイル読み込み
def read_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()


# 実行例
if __name__ == '__main__':

    # テキストファイルの入出力
    text_file = 'example.txt'
    write_text_file(text_file, "Hello, world!\nThis is a test.")
    print("テキスト読み込み:", read_text_file(text_file))
    
    # CSVファイルの入出力
    csv_file = 'example.csv'
    header = ['Name', 'Age', 'Country']
    data = [
        ['Alice', 30, 'USA'],
        ['Bob', 25, 'UK'],
        ['Charlie', 35, 'Canada']
    ]

    write_csv_file(csv_file, header, data)
    csv_header, csv_data = read_csv_file(csv_file)
    print("CSV読み込み:", csv_header, csv_data)
    
    # JSONファイルの入出力
    json_file = 'example.json'
    json_data = {
        "name": "Alice",
        "age": 30,
        "country": "USA"
    }
    write_json_file(json_file, json_data)
    print("JSON読み込み:", read_json_file(json_file))
