import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    try:
        body = event
        
        if 'Post_id' not in body or 'Usuario_id' not in body:
            return generate_response(400, {'message': 'Faltan claves Post_id o Usuario_id en el cuerpo de la solicitud'})
        
        try:
            post_id = int(body['Post_id'])
            usuario_id = body['Usuario_id']
        except ValueError:
            return generate_response(400, {'message': 'Post_id debe ser un número y Usuario_id debe ser una cadena.'})
        
        dynamodb = boto3.resource('dynamodb')
        post_table = dynamodb.Table('Post')
        
        try:
            response = post_table.query(
                KeyConditionExpression=Key('Post_id').eq(post_id) & Key('Usuario_id').eq(usuario_id)
            )
            if 'Items' not in response or len(response['Items']) == 0:
                return generate_response(404, {'message': 'Post no encontrado.'})
            
            item = response['Items'][0]
            likes_actuales = int(item.get('Likes', 0))

        except ClientError as e:
            return generate_response(500, {'message': 'Error al obtener los datos del post', 'error': str(e)})

        nueva_cantidad_likes = likes_actuales + 1

        try:
            response = post_table.update_item(
                Key={'Post_id': post_id, 'Usuario_id': usuario_id},
                UpdateExpression='SET Likes = :val',
                ExpressionAttributeValues={':val': nueva_cantidad_likes},
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            return generate_response(500, {'message': 'Error al actualizar los datos del post', 'error': str(e)})

        return generate_response(200, {'message': 'Likes incrementados correctamente', 'nueva_cantidad': nueva_cantidad_likes})

    except Exception as e:
        return generate_response(500, {'message': 'Error inesperado', 'error': str(e)})

def generate_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
        'body': json.dumps(body)
    }
