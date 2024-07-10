import json
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal

# Obtener todos los registros de la tabla Post
def lambda_handler(event, context):
    # Conectar a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    post_table = dynamodb.Table('Post')

    try:
        response = post_table.scan()
        posts = response.get('Items', [])
    except ClientError as e:
        print(f"ClientError: {e}")
        return generate_response(500, {'message': 'Error al obtener las publicaciones', 'error': str(e)})
    except Exception as e:
        print(f"Exception: {e}")
        return generate_response(500, {'message': 'Error interno del servidor', 'error': str(e)})

    return generate_response(200, posts)

def generate_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'PUT, GET, POST, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
        'body': json.dumps(body, default=decimal_default)
    }

def decimal_default(obj):
    if isinstance(obj, Decimal):
        # Convertir a int si no tiene parte fraccionaria, de lo contrario convertir a float
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
