import json
from django.db import models

import pika


def update_data_signal(queue_name, callback):#Esta funcion se conecta con RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('0.0.0.0'))#Paramtro de la coneccion
    channel = connection.channel()#Abre la conexion
    channel.queue_declare(queue=queue_name, durable=True)#Se declara el nombre de la cola

    def basic_publish(data: dict):#Guarda parametro de la cola
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(data),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )

    callback(basic_publish)#Ejecuta callback de data o user 
    connection.close()#Cierra la coneccion termina la cola 