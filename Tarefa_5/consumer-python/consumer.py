import pika
import json

def callback(ch, method, properties, body):
    data = json.loads(body)
    nota1 = data['nota1']
    nota2 = data['nota2']
    
    # Cálculo da média na escala 0-100
    media = round((nota1 * 2 + nota2 * 3) / 5, 2)

    if media >= 60:
        situacao = "Aprovado"
    elif media >= 20:
        situacao = "Prova Final"
    else:
        situacao = "Reprovado"

    print(f"📩 Mensagem recebida: {data} | Média: {media} | Situação: {situacao}")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queue = 'notas'
channel.queue_declare(queue=queue, durable=True)

print("👂 Aguardando mensagens. CTRL+C para sair")
channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

channel.start_consuming()