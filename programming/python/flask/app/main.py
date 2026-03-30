import json
import boto3
from flask import Flask, render_template, request, jsonify
import service
import logging
import os

# # ログディレクトリ作成
# os.makedirs('/opt/log', exist_ok=True)

# # Flaskのアクセスログ設定
# access_log_path = '/opt/log/access.log'
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s %(levelname)s %(message)s',
#     handlers=[logging.FileHandler(access_log_path, encoding='utf-8'), logging.StreamHandler()]
# )

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'result':'OK'}), 200

@app.route('/health', methods=['GET'])
def health():
    return "Hello, world!"

@app.route('/orders', methods=['GET'])
def get_order():
    items = service.get_data()
    return render_template('index.html', items=items)


@app.route('/orders', methods=['POST'])
def post_order():   
    id = request.form['id']
    quantity = request.form['quantity']
    data = {
        'id': id,
        'quantity': quantity,
    }

    ## ボディ
    ## 辞書型で取得
    # print(request.form.to_dict())

    ## JSON 形式の取得
    # print(request.get_json())

    ## データをそのまま受け取る
    # base64_data = request.get_data()

    # # formからファイルデータを取得
    # file = request.files['file']

    ## クエリ文字列
    # id = request.args.get('id')
    # quantity = request.args.get('quantity')
    # args = request.args.to_dict()
    # print(args)

    response = service.post_data(data)    
    return jsonify({'message': 'created'}), 201


@app.route('/orders/<int:id>', methods=['PUT']) # idが文字列の場合 → <id>
def put_order(id):   
    data = request.get_json()
    response = service.put_data(data)
    return jsonify({'id':id}), 204


@app.route('/orders/<int:id>', methods=['DELETE']) # idが文字列の場合 → <id>
def delete_order(id):   
    response = service.delete_data(id)
    return jsonify({'id':id}), 204


if __name__ == '__main__':  
    # # ログの出力
    # werkzeug_logger = logging.getLogger('werkzeug')
    # werkzeug_logger.setLevel(logging.INFO)
    # for h in logging.getLogger().handlers:
    #     werkzeug_logger.addHandler(h)

    app.run(host='0.0.0.0', port=8080, threaded=True)
