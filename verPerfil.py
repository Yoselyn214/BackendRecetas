import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

def lambda_handler(event, context):
    # Obtener el id del usuario de los pathParameters
    path_params = event.get('pathParameters', {})
    user_id = path_params.get('Usuario_id')
    
    if not user_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'ID de usuario no proporcionado en los parámetros de la ruta'})
        }
    
    # Conectar a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    user_table = dynamodb.Table('User')
    
    try:
        response = user_table.query(
            KeyConditionExpression=Key('Usuario_id').eq(int(user_id))
        )
        
        if 'Items' not in response or not response['Items']:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Usuario no encontrado'})
            }
        else:
            data = response.get('Items', [])
            
            # Serializar datos a JSON
            return {
                'statusCode': 200,
                'body': json.dumps(data, default=decimal_default)
            }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al obtener los datos', 'error': str(e)})
        }

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError