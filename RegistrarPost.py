import json
import boto3
import base64
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Asume que el cuerpo de la solicitud contiene un JSON con 'Contenido', 'Usuario_id', 'Likes', 'Fecha', 'Hora' y 'Imagen' (en base64)
    body = event
    bucket_name = 'imagenessoftware'
    image_data = base64.b64decode(body['Imagen'])
    image_key = f"images/post_{body['Usuario_id']}_{body['Fecha']}_{body['Hora']}.jpg"

    dynamodb = boto3.resource('dynamodb')
    post_table = dynamodb.Table('Post')
    counter_pos = dynamodb.Table('CounterPosts')

    try:
        # Incrementar el contador y obtener el nuevo Post_id
        response = counter_pos.update_item(
            Key={'CounterPost': 'UserPost'},
            UpdateExpression='ADD CounterValue :increment',
            ExpressionAttributeValues={':increment': 1},
            ReturnValues='UPDATED_NEW'
        )
        Post_id = response['Attributes']['CounterValue']
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al obtener el siguiente Post_id', 'error': str(e)})
        }

    try:
        # Subir la imagen a S3
        s3.put_object(Bucket=bucket_name, Key=image_key, Body=image_data, ContentType='image/jpeg')
        image_url = f"https://{bucket_name}.s3.amazonaws.com/{image_key}"
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al subir la imagen a S3', 'error': str(e)})
        }

    Post = {
        'Post_id': int(Post_id),
        'Usuario_id': int(body['Usuario_id']),
        'Contenido': body['Contenido'],
        'Imagen': image_url,
        'Likes': int(body['Likes']),
        'Fecha': body['Fecha'],
        'Hora': body['Hora']
    }

    try:
        # Guardar los datos del post en DynamoDB
        response = post_table.put_item(Item=Post)
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al guardar los datos del Post', 'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Post registrado exitosamente'})
    }