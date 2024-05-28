from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

def main():
    try:
        # Gerar a chave
        chave = get_random_bytes(16)  # AES usa chaves de 16 bytes (128 bits)
        print("Chave:", base64.b64encode(chave).decode())

        texto_aberto = "the quick brown fox jumps over the lazy dog"
        
        # Criptografar
        cifrador = AES.new(chave, AES.MODE_ECB)
        texto_preenchido = pad(texto_aberto.encode(), AES.block_size)
        texto_cifrado = cifrador.encrypt(texto_preenchido)
        
        print("Texto aberto:", len(texto_aberto), texto_aberto)
        print("Texto cifrado:", len(texto_cifrado), base64.b64encode(texto_cifrado).decode())

        # Descriptografar
        texto_recuperado = unpad(cifrador.decrypt(texto_cifrado), AES.block_size)
        
        print("Texto recuperado:", texto_recuperado.decode())

    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")

if __name__ == "__main__":
    main()
