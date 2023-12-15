import pika
import hashlib
import os
import subprocess


def calculate_md5(data):
    hasher = hashlib.md5()
    hasher.update(data)
    md5_hash = hasher.hexdigest()
    return md5_hash


def process_cache_clear_request(ch, method, properties, body):
    image_path = body
    # Xử lý yêu cầu xóa cache ở đây
    hash_path_image = calculate_md5(image_path)
    print("Received cache clear request for image:", image_path)
    path_file = f"/var/nginx/cache/{str(hash_path_image[-1])}/{str(hash_path_image[-3]+hash_path_image[-2])}/{hash_path_image}"
    print(path_file)
    print("delete...")
    try:
        command = ['sudo', 'rm', path_file]

        # Nhập mật khẩu sudo
        sudo_password = 1250

        # Sử dụng đối số 'input' để gửi mật khẩu sudo
        completed_process = subprocess.run(
            command, input=sudo_password, text=True, capture_output=True)

    except Exception:
        pass
    else:
        print("Da xoa##################################")
    # Xác nhận đã xử lý tin nhắn
    ch.basic_ack(delivery_tag=method.delivery_tag)


def run_subscriber():
    # Kết nối tới RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Định nghĩa queue
    queue_name = 'cache_clear_queue'
    channel.queue_declare(queue=queue_name)

    # Thiết lập hàm xử lý tin nhắn cho hàng đợi
    channel.basic_consume(
        queue=queue_name, on_message_callback=process_cache_clear_request)

    # Bắt đầu lắng nghe và xử lý tin nhắn từ hàng đợi
    print("Waiting for cache clear requests...")
    channel.start_consuming()


run_subscriber()
