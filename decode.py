from PIL import Image

def decode_image(image_path):
    # Membuka gambar dan memulai pembacaan pesan
    image = Image.open(image_path)
    pixels = image.load()

    binary_message = ""
    for y in range(image.height):
        for x in range(image.width):
            r, g, b = pixels[x, y][:3]  # Mengambil hanya nilai R, G, B
            binary_message += str(r & 1)
            binary_message += str(g & 1)
            binary_message += str(b & 1)

            # Mengecek stop signal
            if binary_message[-16:] == '1111111111111110':
                break
        else:
            continue
        break

    # Mengubah biner ke teks
    binary_message = binary_message[:-16]
    message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
    return message

output_image_path = 'encoded_image.png'

decoded_message = decode_image(output_image_path)
print("Pesan yang disisipkan:", decoded_message)