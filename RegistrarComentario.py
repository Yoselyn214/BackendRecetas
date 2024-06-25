import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Obtener los datos del cuerpo de la solicitud POST
    body = event
    
    # Verificar que todas las claves necesarias estén presentes en el cuerpo de la solicitud
    required_keys = ['Usuario_id', 'Post_id', 'Contenido', 'Fecha', 'Hora']
    missing_keys = [key for key in required_keys if key not in body]
    
    if missing_keys:
        return generate_response(400, {'message': f'Faltan las siguientes claves en el cuerpo de la solicitud: {", ".join(missing_keys)}'})
    
    # Extraer y convertir los valores de DynamoDB a los tipos esperados
    try:
        usuario_id = int(body['Usuario_id']['N'])  # Asegurarse de que Usuario_id es un entero
        post_id = int(body['Post_id']['N'])
        likes = int(body.get('Likes', {'N': 0})['N'])  # Asignar un valor predeterminado si 'Likes' no está presente
        comentario_id = int(body['Comentario_id']['N'])
    except (ValueError, KeyError, TypeError) as e:
        return generate_response(400, {'message': 'Error en la conversión de datos', 'error': str(e)})
    
    # Conectar a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    comment_table = dynamodb.Table('Comentario')
    counter_table = dynamodb.Table('CounterComentarios') 
    
    try:
        response = counter_table.update_item(
            Key={'Comentarios_Count': 'ComentarioCounter'},
            UpdateExpression='ADD CounterValue :increment',
            ExpressionAttributeValues={':increment': 1},
            ReturnValues='UPDATED_NEW'
        )
        comentario_id = response['Attributes']['CounterValue']
    except ClientError as e:
        return generate_response(500, {'message': 'Error al obtener el siguiente Comentario_id', 'error': str(e)})
    
    # Extraer datos del cuerpo de la solicitud
    comentario = {
        'Comentario_id': comentario_id,
        'Usuario_id': usuario_id,
        'Post_id': post_id,
        'Contenido': body['Contenido']['S'],
        'Likes': likes,
        'Fecha': body['Fecha']['S'],
        'Hora': body['Hora']['S']
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




  
