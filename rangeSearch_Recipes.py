import json
import boto3
from boto3.dynamodb.conditions import Attr
from decimal import Decimal
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Conectar a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    recipe_table = dynamodb.Table('Recetas')
    
    # Extraer valores del cuerpo del evento
    body = event
    cal_max = Decimal(str(body.get('max_calories')))
    cal_min = Decimal(str(body.get('min_calories')))
    
    if cal_min is None or cal_max is None:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Parámetros de calorías faltantes'})
        }

    # Utilizar una expresión de condición para filtrar en DynamoDB
    try:
        response = recipe_table.scan(
            FilterExpression=Attr('Calorias').between(cal_min, cal_max),
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

