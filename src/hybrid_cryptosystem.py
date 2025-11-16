from des_encryption import DESEncryption
from rotor_machine import RotorMachine


class HybridCryptosystem:

    def __init__(self):
        self.rotor_machine = RotorMachine()
        self.des = DESEncryption()

    def encrypt(self, M: str):
        # 1. Encrypt using the rotor machine
        E1 = self.rotor_machine.encrypt(M)
        # 2. Encrypt the result using DES
        E2 = self.des.encrypt(E1)
        return E1, E2  # Encrypted text

        # Time complexity: O(n) where n is the length of the plaintext
        # The rotor machine encryption and decryption operations have a time complexity of O(n)
        # The DES encryption and decryption operations have a time complexity of O(1) since they operate on 64-bit blocks
        # Therefore, the overall time complexity of the encryption and decryption processes is O(n) + O(k) where k is the number of rounds to each block

    def decrypt(self, M: str):
        # 1. Decrypt using DES
        D1 = self.des.decrypt(M)
        # 2. Decrypt the result using the rotor machine
        D2 = self.rotor_machine.decrypt(D1)
        return D1, D2  # Decrypted text

        # Time complexity: O(n) where n is the length of the ciphertext
        # The DES decryption operation has a time complexity of O(1)
        # The rotor machine decryption operation has a time complexity of O(n)
        # Therefore, the overall time complexity of the decryption process is O(n) + O(k) where k is the number of rounds to each block


if __name__ == "__main__":
    hybrid_crypto = HybridCryptosystem()
    plaintext = "This is the hybrid cryptosystem test."
    encrypted_text = hybrid_crypto.encrypt(plaintext)
    decrypted_text = hybrid_crypto.decrypt(encrypted_text)

    print(f"Plaintext: {plaintext}")
    print(f"Encrypted Text: {encrypted_text}")
    print(f"Decrypted Text: {decrypted_text}")
