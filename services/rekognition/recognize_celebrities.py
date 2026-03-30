import boto3

rekognition = boto3.client('rekognition')

def recognize_celebrities(bucket, key):
    response = rekognition.recognize_celebrities(
        Image={
            'S3Object':{
                'Bucket':bucket,
                'Name':key
                }
            }
        )
    return response


def lambda_handler(event, context):
    bucket = 'lab2-s3'
    key = 'test.jpg'
    recognize_celebrities_response = recognize_celebrities(bucket, key)

    celebrity_list = []
    for celebrity in recognize_celebrities_response['CelebrityFaces']:
        celebrity_dict = {}
        celebrity_dict['Name'] = celebrity['Name']
        celebrity_dict['Id'] = celebrity['Id']
        celebrity_dict['Emotions'] = celebrity['Face']['Emotions'][0]['Type']
        celebrity_dict['KnownGender'] = celebrity['KnownGender']['Type']
        celebrity_dict['Smile'] = celebrity['Face']['Smile']['Value']
        celebrity_dict['Urls'] = celebrity['Urls']
        celebrity_list.append(celebrity_dict)
    print(celebrity_list)

    return {
        'statusCode': 200,
        'body': 'OK'
    }