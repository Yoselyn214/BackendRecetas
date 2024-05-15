import json
import boto3

def lambda_handler(event, context):
    # Obtener los datos del cuerpo de la solicitud POST
    body = event

    # Conectar a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('User')  # Nombre de la tabla de usuarios

    # Extraer datos del cuerpo de la solicitud
    usuario = {
        'Usuario_id': int(body['Usuario_id']),
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

    # Guardar los datos en la tabla de usuarios
    response = table.put_item(Item=usuario)

    # Devolver la respuesta
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Usuario registrado exitosamente'})
    }