import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    # Obtener el nombre del cuerpo de la solicitud
    body = event
    nombre = body['Nombre']
    
    if not nombre:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Nombre no proporcionado'})
        }

    # Conectar a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    recipe_table = dynamodb.Table('Recetas')

    try:
        # Usar query con el índice secundario global
        response = recipe_table.query(
            IndexName='Nombre-index',
            KeyConditionExpression=Key('Nombre').eq(nombre),
            Limit=100
        )
        recipes = response.get('Items', [])
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al obtener las publicaciones', 'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': recipes
    }
