from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

class ImageDecryptor:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv
    
    def decode_image(self, image_path):
        """Extract hidden message from image using LSB steganography"""
        img = Image.open(image_path)
        binary_message = self._extract_binary_message(img)
        return self._binary_to_text(binary_message)
    
    def _extract_binary_message(self, img):
        """Extract binary message from image pixels"""
        binary_message = ""
        for x in range(img.width):
            for y in range(img.height):
                pixel = list(img.getpixel((x, y)))
                for color in range(3):  # RGB channels
                    binary_message += str(pixel[color] & 1)
        return binary_message
    
    def _binary_to_text(self, binary_message):
        """Convert binary message to text"""
        message = ""
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i + 8]
            if byte == '11111111':  # End marker
                break
            message += chr(int(byte, 2))
        return message

    def decrypt_message(self, encrypted_message):
        """Decrypt message using AES-CBC"""
        iv_bytes = base64.b64decode(self.iv)
        ct_bytes = base64.b64decode(encrypted_message)
        cipher = AES.new(self.key, AES.MODE_CBC, iv_bytes)
        return unpad(cipher.decrypt(ct_bytes), AES.block_size).decode('utf-8')

def main():
    # Configuration
    KEY = b'\xc6\xbeX\xdd-b\xed\x95\x7f\xcdm^\x7f\xb5\x85\xb1'
    IV = '4p/J/Spx2efDZthaNwfKPA=='
    IMAGE_PATH = 'output/image_20241103_153529_tRCLOte1.png'
    
    # Process
    decryptor = ImageDecryptor(KEY, IV)
    encoded_message = decryptor.decode_image(IMAGE_PATH)
    decrypted_message = decryptor.decrypt_message(encoded_message)
    
    # Output results
    print(f'Encrypted Message: {encoded_message}')
    print(f'Decrypted: {decrypted_message}')

if __name__ == '__main__':
    main()