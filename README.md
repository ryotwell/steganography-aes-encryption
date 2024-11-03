# Steganography with AES Encryption

This project implements a combination of steganography and cryptography. It allows you to hide encrypted messages inside images using the Least Significant Bit (LSB) method. The messages are encrypted using the AES (Advanced Encryption Standard) algorithm.

## Features

- **Encode Messages**: Insert encrypted messages into an image.
- **Decode Messages**: Retrieve encrypted messages from the image.
- **Encrypt/Decrypt Messages**: Use AES to encrypt and decrypt messages.
- **IV Handling**: Initialization Vector (IV) is also embedded in the image for decryption.

## Requirements

- Python 3.x
- Pillow
- PyCryptodome

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ryotwell/steganography-aes-encryption.git
   cd steganography-aes-encryption
