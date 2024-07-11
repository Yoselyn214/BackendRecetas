import json
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal

# Función personalizada para convertir Decimal a float/int
def decimal_default(obj):
    if isinstance(obj, Decimal):
        # Convertir a int si no tiene parte fraccionaria, de lo contrario convertir a float
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    raise TypeError

# Obtener todos los registros de la tabla User
def lambda_handler(event, context):
    # Conectar a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    user_table = dynamodb.Table('User')

    try:
        response = user_table.scan()
        users = response.get('Items', [])
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al obtener los usuarios', 'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            }
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'Items': users}, default=decimal_default),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            
        },
    }
