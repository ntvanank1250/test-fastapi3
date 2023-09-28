import urllib.parse

path_image = "/static/images/download.jpeg"

# Xử lý giá trị đầu vào
processed_path_image = path_image.lstrip("/")

# Mã hóa giá trị với ký tự `.` được mã hóa
encoded_path_image = urllib.parse.quote(processed_path_image, safe="").replace(".", "%2E")
print(processed_path_image)
print(encoded_path_image)

encoded_path_image = "static%2Fimages%2Fdownload%2Ejpeg"

# Giải mã giá trị
decoded_path_image = urllib.parse.unquote(encoded_path_image)

print(decoded_path_image)