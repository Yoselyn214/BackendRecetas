import json
import boto3

def lambda_handler(event, context):
    # Obtener los parámetros de la solicitud GET
    correo_electronico = event['Correo_electronico']
    password = event['Contrasena']

    # Conectar a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('User')  # Nombre de tu tabla de usuarios

    # Consultar la base de datos para buscar al usuario por correo electrónico
    response = table.query(
        IndexName='Correo_electronico-index', 
        KeyConditionExpression=boto3.dynamodb.conditions.Key('Correo_electronico').eq(correo_electronico)
    )

    # Verificar si el usuario existe en la base de datos
    if response['Items']:
        # El usuario existe, ahora verifica la contraseña
        user_data = response['Items'][0]
        if user_data['Contrasena'] == password:
            # La contraseña coincide, usuario autenticado
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Usuario autenticado'})
            }
        else:
            # La contraseña no coincide
            return {
                'statusCode': 401,
                'body': json.dumps({'message': 'Contraseña incorrecta'})
            }
    else:
        # El usuario no existe
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Usuario no encontrado'})
        }
