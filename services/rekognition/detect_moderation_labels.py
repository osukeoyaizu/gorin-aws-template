#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3

rekognition = boto3.client('rekognition', region_name='ap-northeast-1')

def moderate_image(bucket, key):
    response = rekognition.detect_moderation_labels(
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
    key = 'test.jpg'
    moderate_image_response=moderate_image(bucket, key)

    moderation_label_list = []
    for label in moderate_image_response['ModerationLabels']:
        label_dict = {}
        label_dict['Name'] = label['Name']
        label_dict['Confidence'] = label['Confidence']
        label_dict['ParentName'] = label['ParentName']
        label_dict['TaxonomyLevel'] = label['TaxonomyLevel']
        moderation_label_list.append(label_dict)
    print(moderation_label_list)

    return {
        'statusCode': 200,
        'body': 'OK'
    }
