import json

def lambda_handler(event, context):
# htmlの内容をbodyとする
    body = """ <!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>test</title>
</head>
<body>
    <H3>test page</H3>
    <div style="display:flex; justify-content:center; ">
        <div style="display:flex; flex-direction:column; width:50%;">
            <p>名前</p>
            <input id="sender" type="text" />
            <p>メッセージ</p>
            <input id="input" type="text" />
            <div style="margin-top:20px; ">
                <button onclick="send()">送信</button>
            </div>
        </div>
    </div>
    <pre id="output"></pre>
    <script>
        var input = document.getElementById('input');
        var sender = document.getElementById('sender');
        var output = document.getElementById('output');
        // 送信ボタンをクリックした時の処理
        function send() {
            output.innerHTML = sender.value + ": " + input.value;
        };
    </script>
</body>
</html>
    """
    return {
            'statusCode': 200,
            'statusDescription': '200 OK',
            'isBase64Encoded': False,
            'headers': {
                'Content-Type': 'text/html; charset=utf-8'
            },
            'body': body
    }
