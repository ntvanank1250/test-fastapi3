import pika


def send_cache_clear_request(path):
    # Kết nối tới RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Định nghĩa queue
    queue_name = 'cache_clear_queue'
    channel.queue_declare(queue=queue_name)
    # Gửi tin nhắn chứa đường dẫn ảnh tới RabbitMQ
    channel.basic_publish(exchange='', routing_key=queue_name, body=path)
    print("Sent cache clear request for image:", path)
    connection.close()
# Gửi yêu cầu xóa cache
