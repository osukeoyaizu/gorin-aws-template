import boto3

rekognition = boto3.client('rekognition')

def detect_protective_equipment(bucket, key):
    response = rekognition.detect_protective_equipment(
        Image={
            'S3Object':{
                'Bucket':bucket,
                'Name':key
                }
            }
        )
    return response


def lambda_handler(event, context):
    bucket = 'my-s3-bucket'
    key = 'test.jpeg'
    detect_protective_equipment_response = detect_protective_equipment(bucket, key)

    ppe_list = []
    for protective_equipment in detect_protective_equipment_response['Persons']:
        ppe_dict = {}
        ppe_dict['Id'] = protective_equipment['Id']
        ppe_dict['BodyParts'] = []
        for body_part  in protective_equipment['BodyParts']:
            if body_part['EquipmentDetections']:
                body_part_dict = {}
                body_part_dict['Name'] = body_part['Name']
                body_part_dict['Type'] = body_part['EquipmentDetections'][0]['Type']
                body_part_dict['Confidence'] = body_part['EquipmentDetections'][0]['Confidence']
                ppe_dict['BodyParts'].append(body_part_dict)
        ppe_list.append(ppe_dict)
    print(ppe_list)

    return {
        'statusCode': 200,
        'body': 'OK'
    }