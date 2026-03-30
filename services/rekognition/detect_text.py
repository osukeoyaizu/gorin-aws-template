import boto3

rekognition = boto3.client('rekognition', region_name='ap-northeast-1')

# 画像内のテキストを検出
def detect_text(bucket, key):
    response = rekognition.detect_text(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
                }
            }
        )
    return response


def lambda_handler(event, context):
    bucket = 'my-s3-bucket'
    key = 'test.jpeg'
    detect_text_response = detect_text(bucket, key)

    text_list = []
    for detectedText in detect_text_response['TextDetections']:
        text_dict = {}
        text_dict['DetectedText'] = detectedText['DetectedText']
        text_dict['Confidence'] = detectedText['Confidence']
        text_list.append(text_dict)
    print(text_list)

    return {
        'statusCode': 200,
        'body': 'OK'
    }