import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from decimal import Decimal

def lambda_handler(event, context):
    # Registrar el evento entrante para depuración
    print("Event: ", json.dumps(event))
    
    # Obtener el id del post de los pathParameters
    path_params = event.get('pathParameters', {})
    post_id = path_params.get('Post_id')
    
    if not post_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'ID del post no proporcionado en los parámetros de la ruta'})
        }

    # Conectar a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    comment_table = dynamodb.Table('Comentario')

    try:
        # Convertir post_id a entero si es necesario
        try:
            post_id = int(post_id)
        except ValueError:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'ID del post debe ser un número'})
            }

        # Realizar la consulta a la tabla Comentario usando el índice
        response = comment_table.query(
            IndexName='Post_id-index',  # Usa el nombre del índice existente
            KeyConditionExpression=Key('Post_id').eq(post_id)
        )
        
        if 'Items' not in response or not response['Items']:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Comentario no encontrado'})
            }
        else:
            comentario = response['Items']
            
            return {
                'statusCode': 200,
                'body': json.dumps(comentario, default=decimal_default)
            }
    except ClientError as e:
        # Registrar el error para depuración
        print("ClientError: ", e)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al obtener el comentario', 'error': str(e)})
        }
    except Exception as e:
        # Registrar cualquier otro error no anticipado
        print("Exception: ", e)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error interno del servidor', 'error': str(e)})
        }

def decimal_default(obj):
    if isinstance(obj, Decimal):
        # Convertir a int si no tiene parte fraccionaria, de lo contrario convertir a float
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    raise TypeError
