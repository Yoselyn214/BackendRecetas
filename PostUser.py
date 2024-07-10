import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from decimal import Decimal

def lambda_handler(event, context):
    # Registrar el evento entrante para depuración
    print("Event: ", json.dumps(event))
    
    # Obtener el id del usuario de los pathParameters
    path_params = event.get('pathParameters', {})
    usuario_id = path_params.get('Usuario_id')
    
    if not usuario_id:
        return generate_response(400, {'message': 'ID del usuario no proporcionado en los parámetros de la ruta'})

    # Conectar a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    post_table = dynamodb.Table('Post')

    try:
        # Convertir usuario_id a entero si es necesario
        try:
            usuario_id = int(usuario_id)
        except ValueError:
            return generate_response(400, {'message': 'ID del usuario debe ser un número'})

        # Realizar la consulta a la tabla Post usando el índice
        response = post_table.query(
            IndexName='Usuario_id-index',  # Usa el nombre del índice existente
            KeyConditionExpression=Key('Usuario_id').eq(usuario_id)
        )
        
        if 'Items' not in response or not response['Items']:
            return generate_response(404, {'message': 'No se encontraron posts para este usuario'})
        else:
            posts = response['Items']
            return generate_response(200, posts)
    except ClientError as e:
        # Registrar el error para depuración
        print("ClientError: ", e)
        return generate_response(500, {'message': 'Error al obtener los posts', 'error': str(e)})
    except Exception as e:
        # Registrar cualquier otro error no anticipado
        print("Exception: ", e)
        return generate_response(500, {'message': 'Error interno del servidor', 'error': str(e)})

def generate_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
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
    raise TypeError("No se puede serializar ", obj)

