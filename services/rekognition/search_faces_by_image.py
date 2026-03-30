import json
import boto3
import base64

rekognition = boto3.client('rekognition')

def create_collection(collection_id):
    """
    顔を保存するコレクションを作成
    """
    try:
        response = rekognition.create_collection(CollectionId=collection_id)
        print(f"Collection '{collection_id}' created.")
    except Exception as e:
        print(f"Collection creation skipped: {e}")

def add_face_to_collection(collection_id, bucket, image, external_id=None):
    """
    指定した画像から顔を検出してコレクションに登録
    """
    response = rekognition.index_faces(
        CollectionId=collection_id,
        Image={'S3Object': {'Bucket': bucket, 'Name': image}},
        ExternalImageId=external_id,
        DetectionAttributes=['DEFAULT']
    )
    print("Faces indexed:")
    for face_record in response['FaceRecords']:
        print(f"  FaceId: {face_record['Face']['FaceId']}")

def search_face_in_collection(collection_id, decoded_data):
    print(decoded_data)
    """
    指定した画像の顔をコレクション内で検索
    """
    response = rekognition.search_faces_by_image(
        CollectionId=collection_id,
        Image={'Bytes': decoded_data},
        FaceMatchThreshold=70,
        MaxFaces=2
    )

    matches = []
    for match in response['FaceMatches']:
        matches.append({
            "FaceId": match['Face']['FaceId'],
            "Similarity": round(match['Similarity'], 2)
        })
    return matches

def lambda_handler(event, context):
    collection_id = 'SampleCollection'
    index_bucket = 'sample-rekognition'
    index_image = 'search_faces_by_image/index_faces/index.jpeg'
    body = json.loads(event['body'])
    base64_data = body['body']

    decoded_data = base64.b64decode(base64_data)

    # 1. コレクション作成
    create_collection(collection_id)

    # 2. 顔を登録
    add_face_to_collection(collection_id, index_bucket, index_image, external_id="user123")

    # 3. 顔検索
    matches = search_face_in_collection(collection_id, decoded_data)

    result = 'No match'
    if matches:
        result = 'match!'

    return {
        "statusCode": 200,
        "body": result
    }

