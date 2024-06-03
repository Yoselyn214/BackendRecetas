import json
import boto3
from botocore.exceptions import ClientError

# Obtener todos los registros de la tabla Post
def lambda_handler(event, context):
    # Conectar a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    comment_table = dynamodb.Table('Post')

    try:
        response = comment_table.scan()
        posts = response.get('Items', [])
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al obtener las publicaciones', 'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': posts
    }