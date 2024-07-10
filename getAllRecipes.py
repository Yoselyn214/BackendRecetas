import json
import boto3
from botocore.exceptions import ClientError

# Obtener todos los registros de la tabla Post
def lambda_handler(event, context):
    # Conectar a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    recipe_table = dynamodb.Table('Recetas')

    try:
        response = recipe_table.scan(Limit=100)
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
