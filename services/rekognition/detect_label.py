import boto3

rekognition = boto3.client('rekognition', region_name='ap-northeast-1')

def detect_labels(bucket, key):
    response = rekognition.detect_labels(
        Image={
            'S3Object':{
                'Bucket':bucket,
                'Name':key
                }
            },
            MaxLabels=10,
        # Uncomment to use image properties and filtration settings
        #Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"],
        #Settings={"GeneralLabels": {"LabelInclusionFilters":["Cat"]},
        # "ImageProperties": {"MaxDominantColors":10}}
        )
    return response


def lambda_handler(event, context):
    bucket = 'my-s3-bucket'
    key = 'test.jpeg'
    detect_labels_response = detect_labels(bucket, key)

    # response['Labels']をlabelに格納し、label['Name]に'A'か'B'があったらlabel['Name']の値をlabel_checkに格納する
    label_check = [label['Name'] for label in detect_labels_response['Labels'] if 'A' in label['Name'] or 'B' in label['Name']]

    label_list = []
    for label in detect_labels_response['Labels']:
        label_dict = {}
        label_dict['Name'] = label['Name']
        label_dict['Confidence'] = label['Confidence']
        label_list.append(label_dict)
    print(label_list)

    return {
        'statusCode': 200,
        'body': 'OK'
    }

