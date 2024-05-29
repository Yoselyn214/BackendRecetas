import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    #Obtener los datos del cuerpo de la solicitud POST
    body = event
    
    #Conectar a DynamoDB
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
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al obtener el siguiente Comentario_id', 'error': str(e)})
        }
    
    #Extraer datos del cuerpo de la solicitud
    comentario = {
        'Comentario_id': int(comentario_id),
        'Usuario_id': body['Usuario_id'],
        'Post_id': body['Post_id'],
        'Contenido': body['Contenido'],
        'Likes': int(body['likes']),  # Convertir a entero
        'Fecha': body['Fecha'],
        'Hora': body['Hora']
    }
    
    #Guardar los datos en la tabla de comentarios
    try:
        response = comment_table.put_item(Item=comentario)
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al guardar los datos del comentario', 'error': str(e)})
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Comentario '})
    }