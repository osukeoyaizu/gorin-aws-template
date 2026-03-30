import json
from lambda_function import lambda_handler


def test_status_code_is_200():
    response = lambda_handler({}, {})
    assert response["statusCode"] == 200


def test_body_is_valid_json():
    response = lambda_handler({}, {})
    body = json.loads(response["body"])
    assert isinstance(body, dict)


def test_body_message_is_hello():
    response = lambda_handler({}, {})
    body = json.loads(response["body"])
    assert body.get("message") == "hello"

