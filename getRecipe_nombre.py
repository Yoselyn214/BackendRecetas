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
    
    result = []
    for elem in recipes:
        registro = elem.get("Nombre")
        if (event["Nombre"]).lower() in registro.lower():
            result.append(elem)

    return {
        'statusCode': 200,
        'body': result
    }
