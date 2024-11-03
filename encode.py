from PIL import Image

def encode_image(image_path, message, output_image_path):
    try:
        # Membuka gambar dan mengubahnya menjadi mode RGB jika diperlukan
        image = Image.open(image_path).convert("RGB")  # Pastikan dalam mode RGB untuk mempermudah
        pixels = image.load()

        # Menyisipkan pesan di bit paling rendah setiap piksel
        binary_message = ''.join(format(ord(c), '08b') for c in message) + '1111111111111110'  # Stop signal
        message_length = len(binary_message)
        idx = 0

        for y in range(image.height):
            for x in range(image.width):
                if idx < message_length:
                    # Dapatkan nilai RGB (abaikan alpha jika ada)
                    pixel = pixels[x, y]
                    r, g, b = pixel[:3]  # Mengambil hanya nilai R, G, B
                    
                    # Memodifikasi bit paling rendah pada komponen merah (r)
                    r = (r & 0xFE) | int(binary_message[idx])
                    idx += 1
                    
                    if idx < message_length:
                        # Memodifikasi bit paling rendah pada komponen hijau (g)
                        g = (g & 0xFE) | int(binary_message[idx])
                        idx += 1
                    
                    if idx < message_length:
                        # Memodifikasi bit paling rendah pada komponen biru (b)
                        b = (b & 0xFE) | int(binary_message[idx])
                        idx += 1

                    # Menyimpan kembali piksel yang sudah dimodifikasi
                    pixels[x, y] = (r, g, b)

        image.save(output_image_path)

        print("Pesan telah disisipkan ke dalam gambar.")
    except Exception as FileNotFoundError:
        print("File tidak ditemukan. Pastikan file gambar ada di direktori yang sama.")

image_path = 'image.png'
output_image_path = 'encoded_image.png'
message = 'Ini adalah pesan rahasia!'

encode_image(image_path, message, output_image_path)