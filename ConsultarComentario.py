import json
import boto3
from botocore.exceptions import ClientError
# Obtener comentario según su id
def lambda_handler(event, context):
    Post_id = event['Post_id']

    # Conectar a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    comment_table = dynamodb.Table('Comentario')
        
    try:
        response = comment_table.query(
            IndexName='Post_id-index', 
            KeyConditionExpression=boto3.dynamodb.conditions.Key('Post_id').eq(Post_id)
            )
        # Verificar si el comentario existe
        if response['Items']:
            comentario = response['Items']
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Comentario no encontrado'})
            }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al obtener el comentario', 'error': str(e)})
        }

    return {
        'statusCode': 200,
        'comentarios':comentario
    }