import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    #Obtener los datos del cuerpo de la solicitud POST
    body = event
    
    #Conectar a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    user_table = dynamodb.Table('User')
    counter_table = dynamodb.Table('Counters') 

    try:
        response = counter_table.update_item(
            Key={'CounterName': 'UserCounter'},
            UpdateExpression='ADD CounterValue :increment',
            ExpressionAttributeValues={':increment': 1},
            ReturnValues='UPDATED_NEW'
        )
        usuario_id = response['Attributes']['CounterValue']
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al obtener el siguiente Usuario_id', 'error': str(e)})
        }
    
    # Verifica si el correo electrónico existe
    response = user_table.query(
        IndexName='Correo_electronico-index', 
        KeyConditionExpression=boto3.dynamodb.conditions.Key('Correo_electronico').eq(body["Correo_electronico"])
    )
    
    if response['Items']:
        return {
                'statusCode': 401,
                'body': json.dumps({'message': 'Correo electronico ya existente'})
            }
    
    response_1 = user_table.query(
        IndexName='Username-index', 
        KeyConditionExpression=boto3.dynamodb.conditions.Key('Username').eq(body["Username"])
    )
    # Verificar si el usuario existe en la base de datos
    if response_1['Items']:
        return {
            'statusCode': 401,
            'body': json.dumps({'message': 'Nombre de usuario ya existente'})
        }
    
    
    #Extraer datos del cuerpo de la solicitud
    usuario = {
        'Usuario_id': int(usuario_id),
        'Username': body['Username'],
        'Correo_electronico': body['Correo_electronico'],
        'Contrasena': body['Contrasena'],
        'Nombre_y_apellidos': body['Nombre_y_apellidos'],
        'Edad': int(body['Edad']),  # Convertir a entero
        'Fecha_de_nacimiento': body['Fecha_de_nacimiento'],
        'Sexo': body['Sexo'],
        'Presentacion': body['Presentacion'],
        'Num_seguidores': int(body['Num_seguidores']),  # Convertir a entero
        'Num_seguidos': int(body['Num_seguidos'])  # Convertir a entero
    }

    #Guardar los datos en la tabla de usuarios
    try:
        response = user_table.put_item(Item=usuario)
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al guardar los datos del usuario', 'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Usuario registrado exitosamente'})
    }
