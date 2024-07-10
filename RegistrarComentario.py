import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Obtener los datos del cuerpo de la solicitud POST
    body = event
    
    # Verificar que todas las claves necesarias estén presentes en el cuerpo de la solicitud
    required_keys = ['Usuario_id', 'Post_id', 'Contenido', 'Fecha', 'Hora', 'Username']
    missing_keys = [key for key in required_keys if key not in body]
    
    if missing_keys:
        return generate_response(400, {'message': f'Faltan las siguientes claves en el cuerpo de la solicitud: {", ".join(missing_keys)}'})
    
    # Extraer y convertir los valores a los tipos esperados
    try:
        usuario_id = int(body['Usuario_id'])
        post_id = int(body['Post_id'])
        likes = int(body.get('Likes', 0))  # Asignar un valor predeterminado si 'Likes' no está presente
        username = body['Username']
    except (ValueError, KeyError, TypeError) as e:
        return generate_response(400, {'message': 'Error en la conversión de datos', 'error': str(e)})
    
    # Conectar a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    user_table = dynamodb.Table('User')
    comment_table = dynamodb.Table('Comentario')
    counter_table = dynamodb.Table('CounterComentarios') 
    
    # Verificar si el usuario existe en la tabla User
    try:
        user_response = user_table.get_item(Key={'Usuario_id': usuario_id, 'Username': username})
        if 'Item' not in user_response:
            return generate_response(400, {'message': 'Usuario no existe en la tabla User'})
    except ClientError as e:
        return generate_response(500, {'message': 'Error al verificar el usuario', 'error': str(e)})
    
    try:
        # Incrementar el contador y obtener el nuevo Comentario_id
        response = counter_table.update_item(
            Key={'Comentarios_Count': 'ComentarioCounter'},
            UpdateExpression='ADD CounterValue :increment',
            ExpressionAttributeValues={':increment': 1},
            ReturnValues='UPDATED_NEW'
        )
        comentario_id = response['Attributes']['CounterValue']
    except ClientError as e:
        return generate_response(500, {'message': 'Error al obtener el siguiente Comentario_id', 'error': str(e)})
    
    # Preparar los datos del comentario para guardarlos en la tabla de comentarios
    comentario = {
        'Comentario_id': comentario_id,
        'Usuario_id': usuario_id,
        'Post_id': post_id,
        'Contenido': body['Contenido'],
        'Likes': likes,
        'Fecha': body['Fecha'],
        'Hora': body['Hora']
    }
    
    # Guardar los datos en la tabla de comentarios
    try:
        response = comment_table.put_item(Item=comentario)
    except ClientError as e:
        return generate_response(500, {'message': 'Error al guardar los datos del comentario', 'error': str(e)})
    
    return generate_response(200, {'message': 'Comentario guardado exitosamente'})

def generate_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'PUT',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
        'body': json.dumps(body)
    }
