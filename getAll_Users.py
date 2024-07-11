import json
import boto3
from botocore.exceptions import ClientError

# Obtener todos los registros de la tabla User
def lambda_handler(event, context):
    # Conectar a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    recipe_table = dynamodb.Table('User')

    try:
        response = recipe_table.scan()
        recipes = response.get('Items', [])
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al obtener los usuarios', 'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': recipes
    }