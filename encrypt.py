from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

def encode_image(image_path, message, output_path):
    img = Image.open(image_path)
    encoded = img.copy()
    binary_message = ''.join(format(ord(i), '08b') for i in message) + '1111111111111110'  # Delimiter
    data_index = 0

    for x in range(img.width):
        for y in range(img.height):
            pixel = list(img.getpixel((x, y)))
            for i in range(3):  # Untuk RGB
                if data_index < len(binary_message):
                    pixel[i] = (pixel[i] & ~1) | int(binary_message[data_index])
                    data_index += 1
            encoded.putpixel((x, y), tuple(pixel))
            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break

    encoded.save(output_path)
    print('Pesan berhasil disisipkan ke dalam gambar.')

# Fungsi untuk enkripsi pesan menggunakan AES
def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv, ct

# Fungsi untuk dekripsi pesan menggunakan AES
def decrypt_message(key, iv, ct):
    iv = base64.b64decode(iv)
    ct = base64.b64decode(ct)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
    return pt

image_path          = 'image.png'
output_image_path   = 'output_image.png'
secret_message      = 'This is a secret message.'

key = get_random_bytes(16)  # Kunci 16 bytes untuk AES-128
iv, encrypted_message = encrypt_message(key, secret_message)

# Menyisipkan pesan terenkripsi ke dalam gambar
encode_image(image_path, encrypted_message, output_image_path)

print( f'\nKey    : {key}' )
print( f'IV     : {iv}' )
