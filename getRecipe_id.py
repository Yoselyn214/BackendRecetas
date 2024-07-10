import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

def lambda_handler(event, context):
    # Obtener el id del usuario de los pathParameters
    path_params = event.get('pathParameters', {})
    receta_id = path_params.get('Receta_id')
    
    if not receta_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'ID de receta no proporcionado en los parámetros de la ruta'})
        }
    
    # Conectar a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    user_table = dynamodb.Table('Recetas')
    
    try:
        response = user_table.query(
            KeyConditionExpression=Key('Receta_id').eq(int(receta_id))
        )
        
        if 'Items' not in response or not response['Items']:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Receta no encontrada'})
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