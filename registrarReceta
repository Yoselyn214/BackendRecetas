import json
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal

def lambda_handler(event, context):
    # Obtener los datos del cuerpo de la solicitud POST
    body = event
    
    # Verificar que todas las claves necesarias estén presentes en el cuerpo de la solicitud
    required_keys = ['Nombre', 'Tipo', 'Descripcion_ingredientes', 'Instrucciones', 'Calorias', 'Grasas', 'Proteinas','Imagen','Tiempo_Preparacion']
    missing_keys = [key for key in required_keys if key not in body]
    
    if missing_keys:
        return generate_response(400, {'message': f'Faltan las siguientes claves en el cuerpo de la solicitud: {", ".join(missing_keys)}'})
    
    # Conectar a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    recipe_table = dynamodb.Table('Recetas')
    counter_table = dynamodb.Table('CounterRecetas')
    
    try:
        response = counter_table.update_item(
            Key={'Recetas_Count': 'RecetaCounter'},
            UpdateExpression='ADD CounterValue :increment',
            ExpressionAttributeValues={':increment': 1},
            ReturnValues='UPDATED_NEW'
        )
        receta_id = response['Attributes']['CounterValue']
    except ClientError as e:
        return generate_response(500, {'message': 'Error al obtener la siguiente Receta_id', 'error': str(e)})
    
    # Extraer datos del cuerpo de la solicitud
    receta = {
        'Receta_id': receta_id,
        'Nombre': body['Nombre'],
        'Tipo': body['Tipo'],
        'Descripcion_ingredientes': body['Descripcion_ingredientes'],
        'Instrucciones': body['Instrucciones'],
        'Likes': 0,
        'Calorias': Decimal(str(body['Calorias'])),
        'Grasas': Decimal(str(body['Grasas'])),
        'Proteinas': Decimal(str(body['Proteinas'])),
        'Imagen': body['Imagen'],
        'Tiempo_Preparacion': Decimal(str(body['Tiempo_Preparacion']))
    }
    
    # Guardar los datos en la tabla de comentarios
    try:
        response = recipe_table.put_item(Item=receta)
    except ClientError as e:
        return generate_response(500, {'message': 'Error al guardar los datos de la receta', 'error': str(e)})
    
    return generate_response(200, {'message': 'Receta guardada exitosamente'})

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
