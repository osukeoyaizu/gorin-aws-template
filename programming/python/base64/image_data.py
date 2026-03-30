from flask import Flask, jsonify, request
import base64
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    ans = {'message':'hello'}
    return jsonify(ans)
    
@app.route('/health', methods=['GET'])
def health():
    return 'OK'

@app.route('/add', methods=['POST'])
def post():
        # リクエストボディからデータを取得する
        base64_data = request.get_data()

        # デコードして画像データに戻す
        decoded_data = base64.b64decode(base64_data)

        
        bucket = 'lab2-trial-s3'
        key = 'images/' + str(uuid.uuid4()) + '.jpg'

        response = s3.put_object(Bucket=bucket, Key=key ,Body=decoded_data)
        return 'OK'
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)