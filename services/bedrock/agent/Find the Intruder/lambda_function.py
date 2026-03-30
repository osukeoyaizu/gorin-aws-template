import boto3
import json
import base64
import os
import datetime
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    """
    Main handler for the security system Lambda function.
    This function properly:
    1. Processes images from S3
    2. Uses Rekognition to detect persons
    3. Uses Bedrock for additional image analysis
    4. Implements proper guardrails
    """
    try:
        print(f"REQUEST EVENT: {json.dumps(event)}")
        body = {}
        
        # Check if this is a Bedrock Agent request
        if 'requestBody' in event and 'content' in event['requestBody'] and 'application/json' in event['requestBody']['content']:
            properties = event['requestBody']['content']['application/json'].get('properties', [])
            for prop in properties:
                if 'name' in prop and 'value' in prop:
                    body[prop['name']] = prop['value']
            #print(f"PARSED BEDROCK AGENT REQUEST: {json.dumps(body)}")
        elif 'body' in event:
            if isinstance(event['body'], str):
                try:
                    body = json.loads(event['body'])
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {str(e)}")
                    body = {}
            else:
                body = event['body']
        else:
            body = event
            
        print(f"PARSED BODY: {json.dumps(body)}")
        
        # Input validation
        if not body:
            error_response = {
                "messageVersion": "1.0",
                "response": {
                    "actionGroup": "AwsJamChallengeBedrockAgentActiongroup",
                    "apiPath": "/security",
                    "httpMethod": "POST",
                    "httpStatusCode": 400,
                    "responseBody": {
                        "application/json": {
                            "body": json.dumps({
                                'message': 'Invalid request body',
                                'error': 'Request body is empty or malformed'
                            })
                        }
                    }
                }
            }
            print(f"ERROR: {json.dumps(error_response)}")
            return error_response
        
        # Get the room to analyze
        room = body.get('room', '')
        print(f"***************** ROOM REQUESTED: {room} *********************")
        print(f"Using confidence threshold: {os.environ.get('CONFIDENCE_THRESHOLD', '75.0')}")
        
        valid_rooms = ['bedroom1', 'bedroom2','frontdoor', 'hall', 'garden', 'kitchen']
        if not room or room not in valid_rooms:
            error_response = {
                "messageVersion": "1.0",
                "response": {
                    "actionGroup": "AwsJamChallengeBedrockAgentActiongroup",
                    "apiPath": "/security",
                    "httpMethod": "POST",
                    "httpStatusCode": 404,
                    "responseBody": {
                        "application/json": {
                            "body": json.dumps({
                                'message': 'Invalid room specified',
                                'error': f'Room must be one of: {", ".join(valid_rooms)}',
                                'room': room
                            })
                        }
                    }
                }
            }
            print(f"ERROR: {json.dumps(error_response)}")
            return error_response
        
        try:
            s3_client = boto3.client('s3')
        except Exception as e:
            raise e
            
        bucket_name = os.environ.get('IMAGES_BUCKET', 'house-images')
        #print(f"USING BUCKET: {bucket_name}")
        
        ext = 'png'
        image_key = None
        image_bytes = None
        
        # Try to find the image
        try_key = f"bedrock-agent-mystery/camera/{room}.{ext}"
        #print(f"TRYING IMAGE: {bucket_name}/{try_key}")
        
        try:
            response = s3_client.get_object(Bucket=bucket_name, Key=try_key)
            #print(f"S3 GET_OBJECT RESPONSE: {response}")
            
            image_bytes = response['Body'].read()
            image_key = try_key
            #print(f"IMAGE FETCHED SUCCESSFULLY: {len(image_bytes)} bytes, format: {ext}")
            
            if len(image_bytes) > 20:
                hex_preview = ' '.join([f'{b:02x}' for b in image_bytes[:20]])
                #print(f"IMAGE HEX PREVIEW: {hex_preview}...")

        except ClientError as e:
            if e.response.get('Error', {}).get('Code') == 'NoSuchKey':
                print(f"Image not found with extension {ext}")
            else:
                raise e
        
        if image_bytes is None:
            error_response = {
                "messageVersion": "1.0",
                "response": {
                    "actionGroup": "AwsJamChallengeBedrockAgentActiongroup",
                    "apiPath": "/security",
                    "httpMethod": "POST",
                    "httpStatusCode": 404,
                    "responseBody": {
                        "application/json": {
                            "body": json.dumps({
                                'message': 'Image not found',
                                'error': f"No image found for room '{room}' with extension '{ext}'",
                                'bucket': bucket_name,
                                'room': room
                            })
                        }
                    }
                }
            }
            print(f"IMAGE NOT FOUND ERROR: {json.dumps(error_response)}")
            return error_response
        
        # Rekognition integration with correct confidence threshold
        detection_results = process_image_with_rekognition(image_bytes)
        
        # Bedrock integration for advanced analysis, passing Rekognition results
        bedrock_analysis = analyze_image_with_bedrock(image_bytes, room, detection_results)
        
        # Note: Guardrails are now handled at the Bedrock service level
        # through the SecurityGuardrail resource attached to the agent
        
        formatted_response = format_security_response(room, detection_results, bedrock_analysis)
        print(f"RESPONSE: {json.dumps(formatted_response)}")
        
        if 'requestBody' in event:
            return formatted_response
        else:
            return {
                'statusCode': 200,
                'body': json.dumps(formatted_response)
            }
        
    except Exception as e:
        error_type = type(e).__name__
        error_message = str(e)
        error_response = {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": "AwsJamChallengeBedrockAgentActiongroup",
                "apiPath": "/security",
                "httpMethod": "POST",
                "httpStatusCode": 500,
                "responseBody": {
                    "application/json": {
                        "body": json.dumps({
                            'message': 'Error processing request',
                            'error_type': error_type,
                            'error_details': error_message,
                            'timestamp': datetime.datetime.now().isoformat()
                        })
                    }
                }
            }
        }
        
        print(f"ERROR: {json.dumps(error_response)}")
        return error_response

def process_image_with_rekognition(image_data):
    """
    Process an image using Rekognition to detect persons.
    
    This function:
    1. Calls Amazon Rekognition with the image data
    2. Sets an appropriate confidence threshold from environment variable
    3. Extracts person detection information
    4. Returns structured detection results
    """
    rekognition_client = boto3.client('rekognition')
    
    # Get confidence threshold from environment variable
    confidence_threshold = float(55)
    
    response = rekognition_client.detect_labels(
        Image={'Bytes': image_data},
        MinConfidence=confidence_threshold
    )
    
    # Process person detection
    persons = [label for label in response['Labels'] if label['Name'] == 'Person']

    #print(f"Persons : {persons}")
    #print([label['Name'] for label in response['Labels'] if label['Confidence'] > 55])
    
    # Extract bounding boxes for persons
    person_locations = []
    if persons and 'Instances' in persons[0]:
        for instance in persons[0]['Instances']:
            if 'BoundingBox' in instance:
                person_locations.append(instance['BoundingBox'])
    
    # Use the same confidence threshold for filtering all labels
    results = {
        'persons_detected': len(persons),
        'confidence': persons[0]['Confidence'] if persons else 0,
        'has_person': len(persons) > 0,
        'locations': person_locations,
        'all_labels': [label['Name'] for label in response['Labels'] if label['Confidence'] > confidence_threshold]
    }
    
    print(f"REKOGNITION RESULTS: {json.dumps(results)}")
    return results

def analyze_image_with_bedrock(image_bytes, room_name, rekognition_results):
    """
    Analyze image content using Bedrock models.
    
    This function:
    1. Converts the image to base64 encoding
    2. Prepares a prompt for the Bedrock model, including Rekognition results
    3. Calls the Bedrock model (Claude/Titan)
    4. Processes the response to extract insights
    5. Returns structured analysis results
    """
    # Convert image to base64
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    # Create Bedrock client
    bedrock_client = boto3.client('bedrock-runtime')
    
    # Extract relevant information from Rekognition results
    persons_detected = rekognition_results.get('persons_detected', 0)
    rekognition_confidence = rekognition_results.get('confidence', 0)
    all_labels = rekognition_results.get('all_labels', [])
    
    # Prepare prompt for Claude/Titan, including Rekognition results
    prompt = f"""
    Analyze this image from the {room_name} of a house.
    
    Amazon Rekognition has already analyzed this image with the following results:
    - Persons detected: {persons_detected}
    - Confidence score: {rekognition_confidence}
    - All objects detected: {', '.join(all_labels)}
    
    Based on both the image and the Rekognition results, is there a person in this image?
    Focus only on actual people, not pictures or statues of people.
    Be very specific about the location and appearance of any person detected.
    If a person is identified in the image, flag it as an intruder if they pose any of the traits of an intruder or a robber or doing something suspicious or trying to break into the house, then respond back saying 'intruder found'.
    If there are no intruders identified in the image, respond back stating 'intruder not found'.
    
    Confidence score should be calculated based on this formula: If the intruder is found, then how confident are you that the person is an intruder based on their features. If the intruder is not found, then keep the confidence score between 10 to 30%
    
    Use this format for the response:
    Status:intruder found/intruder not found,Confidence Score:confidence in percentage,Analysis:detailed analysis

    If the Status is intruder not found and rekognition has confidence score of greater than 30%, add a brief explanation in the analysis on why the person is not flagged as an intruder.
    Example : Status: intruder not found, Confidence Score: 20%, Analysis: The image shows a bedroom with a bed, pillows, and various decorative items. The Amazon Rekognition results indicate a person was detected with a confidence score of 74.81%. However, upon close inspection, the detected person appears to be a mannequin or a statue, as it is placed in a prominent location and does not exhibit any movement or living characteristics. No suspicious behavior or signs of an intruder are present in the image.
    """
    
    try:
        message = {
                        "role": "user",
                        "content": [
                            {
                                "text": prompt
                            },
                            {
                                "image": {
                                    "format": "png",
                                    "source": {
                                        "bytes": image_bytes
                                    }
                                }
                            }
                        ]
                    }
        messages = [message]
        # Call Bedrock model
        model_id = os.environ.get('BEDROCK_MODEL_ID', 'amazon.nova-lite-v1:0')
        response = bedrock_client.converse(
            modelId=model_id,
            messages=messages
        )

        response_body = response['output']['message']
        analysis = ""
        for content in response_body['content']:
            analysis += content['text']

        #print(f"BEDROCK ANALYSIS: {analysis}")
        
        has_person = "intruder found" in analysis.lower()
        #analysis = "Status:intruder not found,Confidence Score:95%,Analysis:The image depicts a modern kitchen with white cabinets, wooden floors, and a large central island. There are no visible people in the image. All objects and elements within the kitchen appear to be inanimate, such as kitchen appliances, utensils, and decor items. The kitchen is well-organized, with shelves holding bowls, plates, and kitchenware. The absence of any human presence in the image suggests that there is no intruder."
        try:
            confidence_score = analysis.split(",")[1].split(":")[1]
        except Exception as e:
            confidence_score = 0.0
            print(f"Error extracting confidence score: {str(e)}")
        
        results = {
            'analysis': analysis,
            'has_person': has_person,
            'room': room_name,
            'confidence': confidence_score.strip()
        }
        
        print(f"BEDROCK RESULTS: {json.dumps(results)}")
        return results
    except Exception as e:
        error_result = {
            'analysis': f"Error analyzing image: {str(e)}",
            'has_person': False,
            'room': room_name,
            'confidence': 0.0,
            'error': str(e)
        }
        print(f"BEDROCK ERROR: {json.dumps(error_result)}")
        return error_result


def format_security_response(room, detection_results, bedrock_analysis):
    """
    Format the security response with proper structure.
    
    This function:
    1. Combines results from Rekognition and Bedrock
    2. Calculates confidence scores
    3. Determines if an intruder is present
    4. Formats a comprehensive response with all required fields
    """
    try:
        confidence_threshold = float(os.environ.get('CONFIDENCE_THRESHOLD', '75.0'))
        # Determine if an intruder is present based on both analyses
        rekognition_detected = detection_results.get('has_person', False)
        bedrock_detected = bedrock_analysis.get('has_person', False)
        intruder_detected = False

        # Combined detection logic
        rekognition_confidence = float(detection_results.get('confidence', 0))
        bedrock_confidence = bedrock_analysis.get('confidence', 0)
        try:
            bedrock_confidence = float(bedrock_confidence.replace('%', ''))
        except Exception as e:
            bedrock_confidence = 0.0

        detection_source = "None"
        final_confidence = 0.0
        # Determine if an intruder is detected by either system
        if rekognition_detected and rekognition_confidence >= confidence_threshold:
            detection_source = "Rekognition"
            final_confidence = rekognition_confidence
            print(f"INTRUDER DETECTED BY REKOGNITION: {room}")
            print(f"REKOGNITION CONFIDENCE: {rekognition_confidence}")
    
        # Bedrock combines the input from rekognition and its own analysis to finally arrive at a conclusion if there is an intruder
        if bedrock_detected and bedrock_confidence >= confidence_threshold:
            final_confidence = bedrock_confidence
            detection_source = "Bedrock" + "," + detection_source
            # Remove the extra comma at the end
            detection_source = detection_source[:-1]

            print(f"INTRUDER DETECTED BY BEDROCK: {room}")
            print(f"BEDROCK CONFIDENCE: {bedrock_confidence}")

        # Final confidence and intruder detection is calculated based on the data from both rekognition and bedrock
        if detection_source == "None":
            # No intruder detected
            final_confidence = bedrock_confidence
        if rekognition_confidence >= confidence_threshold and bedrock_confidence >= confidence_threshold:
            # Both systems detected an intruder
            intruder_detected = True
        # If intruder is not found, then use bedrock confidence score
        if not intruder_detected:
            final_confidence = bedrock_confidence
        
        # Format the response - ensure all values are clean and serializable
        timestamp = datetime.datetime.now().isoformat()

        # Clean up the analysis text to ensure it's serializable
        analysis = bedrock_analysis.get('analysis', 'No analysis available')
        if analysis and isinstance(analysis, str):
            analysis = analysis.replace('\u0000', '')
            # Truncate if too long (Bedrock has limits)
            if len(analysis) > 5000:
                analysis = analysis[:5000] + "... (truncated)"

        # Clean up object labels
        all_labels = detection_results.get('all_labels', [])
        if all_labels:
            # Ensure all labels are strings and limit the number
            all_labels = [str(label) for label in all_labels[:50]]

        # Create a summary of the detection results
        if intruder_detected:
            summary = f"INTRUDER DETECTED in {room} by {detection_source} with {final_confidence:.1f}% confidence"
        else:
            summary = f"No intruder detected in {room}. Room is secure."
            
        # Update the confidence threshold parameter with the environment variable value
        try:
            ssm_client = boto3.client('ssm')
            env_threshold = os.environ.get('CONFIDENCE_THRESHOLD', '12.0')
            ssm_client.put_parameter(
                Name='/bedrock-agent-mystery/confidence-threshold',
                Value=env_threshold,
                Type='String',
                Overwrite=True
            )
            print(f"Updated confidence threshold SSM parameter to match environment variable: {env_threshold}")
        except Exception as e:
            print(f"Error updating confidence threshold parameter: {str(e)}")

        detection_response = {
            'room': room,
            'status': 'INTRUDER DETECTED' if intruder_detected else 'Secure',
            'summary': summary,
            'timestamp': timestamp,
            'detection_result': {
                'persons_detected': detection_results.get('persons_detected', 0),
                'has_intruder': intruder_detected,
                'detection_source': detection_source
            },
            'confidence': round(final_confidence, 1),
            'rekognition_confidence': round(rekognition_confidence, 1),
            'bedrock_confidence': round(bedrock_confidence, 1),
            'analysis': analysis,
            'objects_detected': all_labels,
            'room_details': {
                'name': room,
                'objects': all_labels
            },
            'intruder_location': room if intruder_detected else 'unknown'
        }

        final_response = {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": "AwsJamChallengeBedrockAgentActiongroup",
                "apiPath": "/security",
                "httpMethod": "POST",
                "httpStatusCode": 200,
                "responseBody": {
                    "application/json": {
                        "body": detection_response
                    }
                }
            }
        }
        return final_response
    except Exception as e:
        print(f"RESPONSE FORMATTING ERROR: {str(e)}")
        # Return a minimal valid response if there's an error
        return {
            'room': room,
            'status': 'ERROR',
            'timestamp': datetime.datetime.now().isoformat(),
            'error': str(e)
        }