import json
import base64
import boto3

s3 = boto3.client('s3', region_name='ap-northeast-1')

rekognition = boto3.client('rekognition', region_name='ap-northeast-1')

# s3バケットから表情分析
def detect_faces(bucket, key):
    response = rekognition.detect_faces(
                Image={
                    'S3Object': {
                        'Bucket': bucket,
                        'Name': key
                    }
                },
                Attributes=['ALL']    # 取得する属性を指定する 表情のみの情報がほしい場合はEMOTIONSを指定する
            )
    return response


# バイト型データから表情分析
def detect_faces(data):
    response = rekognition.detect_faces(
                Image={
                    'Bytes': data
                },
                Attributes=['ALL']    # 取得する属性を指定する 表情のみの情報がほしい場合はEMOTIONSを指定する
            )  
    return response


# s3バケットからlambdaにファイルダウンロード
def download_file(backet, file_key, local_file_path):
    s3.download_file(backet, file_key, local_file_path)


# ファイルの内容を読む
def read_file(local_file_path):
    with open(local_file_path, 'rb') as f:
        data = f.read()
    return data


def lambda_handler(event, context):
    # s3バケットから表情分析
    bucket = 'my-s3-bucket'
    key = 'my-object-key'
    detect_faces_response = detect_faces(bucket, key)

    # バイト型データから表情分析
    body = event['body']
    image_data = base64.b64decode(body)
    detect_faces_response = detect_faces(image_data)

    # 画像ファイルをダウンロードし、表情分析
    local_file_path = '/tmp/test.jpeg'
    download_file(bucket, key, local_file_path)
    image_data = read_file(local_file_path)
    detect_faces_response = detect_faces(image_data)

    # 全員分の表情分析分析の結果をface_listに格納
    face_list = []
    for faceDetail in detect_faces_response['FaceDetails']:
        emotion_dict = {}
        emotion_dict['Type'] = faceDetail['Emotions'][0]['Type']
        emotion_dict['Confidence'] = faceDetail['Emotions'][0]['Confidence']
        face_list.append(emotion_dict)
    print(face_list)      

    return {
        'statusCode': 200,
        'body': 'OK'
    }