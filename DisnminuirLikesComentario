import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    try:
        # En este caso, el cuerpo de la solicitud parece estar directamente en el evento
        body = event
        
        # Verificar que todas las claves necesarias estén presentes en el cuerpo de la solicitud
        if 'Comentario_id' not in body:
            return generate_response(400, {'message': 'Falta la clave Comentario_id en el cuerpo de la solicitud'})
        
        # Extraer y validar el valor
        try:
            comentario_id = int(body['Comentario_id'])
        except ValueError:
            return generate_response(400, {'message': 'Comentario_id debe ser un número.'})
        
        # Conectar a DynamoDB
        dynamodb = boto3.resource('dynamodb')
        comentario_table = dynamodb.Table('Comentario')
        
        # Obtener la cantidad actual de likes
        try:
            # Realizar una consulta usando solo la clave de partición
            response = comentario_table.query(
                KeyConditionExpression=Key('Comentario_id').eq(comentario_id)
            )
            if 'Items' not in response or len(response['Items']) == 0:
                return generate_response(404, {'message': 'Comentario no encontrado.'})
            
            item = response['Items'][0]  # Asumir que solo hay un comentario con el ID dado
            likes_actuales = int(item.get('Likes', 0))
            usuario_id = item.get('Usuario_id')

        except ClientError as e:
            return generate_response(500, {'message': 'Error al obtener los datos del comentario', 'error': str(e)})

        # Decrementar la cantidad de likes, asegurando que no sea menor a 0
        nueva_cantidad_likes = max(likes_actuales - 1, 0)

        # Guardar la nueva cantidad de likes en la tabla
        try:
            response = comentario_table.update_item(
                Key={'Comentario_id': comentario_id, 'Usuario_id': usuario_id},  # Necesitas proporcionar también el Usuario_id
                UpdateExpression='SET Likes = :val',
                ExpressionAttributeValues={':val': nueva_cantidad_likes},
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            return generate_response(500, {'message': 'Error al actualizar los datos del comentario', 'error': str(e)})

        return generate_response(200, {'message': 'Likes decrementados correctamente', 'nueva_cantidad': nueva_cantidad_likes})

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
