from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import os
from datetime import datetime
import random
import string

class ImageEncryption:
    def __init__(self, image_path: str, output_dir: str = 'output'):
        self.image_path = image_path
        self.output_dir = output_dir
        self.ensure_output_directory()

    def ensure_output_directory(self):
        """Create output directory if it doesn't exist"""
        os.makedirs(self.output_dir, exist_ok=True)

    @staticmethod
    def generate_image_filename(extension: str = 'png') -> str:
        """Generate unique filename with timestamp and random string"""
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f'image_{timestamp}_{random_string}.{extension}'

    def encode_image(self, message: str) -> str:
        """Encode encrypted message into image using LSB steganography"""
        img = Image.open(self.image_path)
        encoded = img.copy()
        binary_message = ''.join(format(ord(i), '08b') for i in message) + '1111111111111110'
        data_index = 0

        for x in range(img.width):
            for y in range(img.height):
                pixel = list(img.getpixel((x, y)))
                for i in range(3):  # RGB channels
                    if data_index < len(binary_message):
                        pixel[i] = (pixel[i] & ~1) | int(binary_message[data_index])
                        data_index += 1
                encoded.putpixel((x, y), tuple(pixel))
                if data_index >= len(binary_message):
                    break
            if data_index >= len(binary_message):
                break

        output_path = os.path.join(self.output_dir, self.generate_image_filename())
        encoded.save(output_path)
        return output_path

class AESCipher:
    def __init__(self, key_size: int = 16):
        """Initialize AES cipher with key size (16 bytes for AES-128)"""
        self.key = get_random_bytes(key_size)

    def encrypt(self, message: str) -> tuple[str, str]:
        """Encrypt message using AES-CBC mode"""
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        return iv, ct

    def decrypt(self, iv: str, ciphertext: str) -> str:
        """Decrypt message using AES-CBC mode"""
        iv_bytes = base64.b64decode(iv)
        ct_bytes = base64.b64decode(ciphertext)
        cipher = AES.new(self.key, AES.MODE_CBC, iv_bytes)
        return unpad(cipher.decrypt(ct_bytes), AES.block_size).decode('utf-8')

def main():
    # Initialize encryption components
    image_path = 'image.png'
    secret_message = 'This is a secret message.'
    
    # Create instances
    aes_cipher = AESCipher()
    image_encryption = ImageEncryption(image_path)
    
    # Encrypt and encode message
    iv, encrypted_message = aes_cipher.encrypt(secret_message)
    output_image = image_encryption.encode_image(encrypted_message)
    
    # Print results
    print('Encryption Results:')
    print(f'Key        : {aes_cipher.key}')
    print(f'IV         : {iv}')
    print(f'Image      : {output_image}')

if __name__ == '__main__':
    main()
