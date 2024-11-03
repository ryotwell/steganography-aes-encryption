from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

def decode_image(image_path):
    img = Image.open(image_path)
    binary_message = ""
    for x in range(img.width):
        for y in range(img.height):
            pixel = list(img.getpixel((x, y)))
            for i in range(3):  # Untuk RGB
                binary_message += str(pixel[i] & 1)
    
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        if byte == '11111111':
            break
        message += chr(int(byte, 2))

    return message

# Fungsi untuk dekripsi pesan menggunakan AES
def decrypt_message(key, iv, ct):
    iv = base64.b64decode(iv)
    ct = base64.b64decode(ct)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
    return pt

key                 = b'b\x80\xd3\x17\xcea\x03[1\xc6\xb7\xb5\xf9\xf0\x12N'
iv                  = 'iqEaX9Jx3DPY35p1YfBSxQ=='
output_image_path   = 'output_image.png'

# Mendekode pesan dari gambar
decoded_encrypted_message = decode_image(output_image_path)
decrypted_message = decrypt_message(key, iv, decoded_encrypted_message)

print(f"Encrypted Message   : {decoded_encrypted_message}")
print(f"Decrypted           : {decrypted_message}")