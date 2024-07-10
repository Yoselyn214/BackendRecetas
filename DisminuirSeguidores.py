import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    try:
        body = event
        
        if 'Usuario_id' not in body:
            return generate_response(400, {'message': 'Falta la clave Usuario_id en el cuerpo de la solicitud'})
        
        try:
            usuario_id = int(body['Usuario_id'])
        except ValueError:
            return generate_response(400, {'message': 'Usuario_id debe ser un número.'})
        
        dynamodb = boto3.resource('dynamodb')
        user_table = dynamodb.Table('User')
        
        try:
            response = user_table.query(
                KeyConditionExpression=Key('Usuario_id').eq(usuario_id)
            )
            if 'Items' not in response or len(response['Items']) == 0:
                return generate_response(404, {'message': 'Usuario no encontrado.'})
            
            item = response['Items'][0]
            current_followers = int(item.get('Num_seguidores', 0))
            username = item.get('Username')

        except ClientError as e:
            return generate_response(500, {'message': 'Error al obtener los datos del usuario', 'error': str(e)})

        new_followers = current_followers - 1

        try:
            response = user_table.update_item(
                Key={'Usuario_id': usuario_id, 'Username': username},
                UpdateExpression='SET Num_seguidores = :val',
                ExpressionAttributeValues={':val': new_followers},
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            return generate_response(500, {'message': 'Error al actualizar los datos del usuario', 'error': str(e)})

        return generate_response(200, {'message': 'Seguidores incrementados correctamente', 'nueva_cantidad': new_followers})

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
